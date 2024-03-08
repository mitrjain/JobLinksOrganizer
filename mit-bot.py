import discord
import os
from dotenv import load_dotenv
import re
from gsheets import Sheets
import gspread
import datetime

load_dotenv()

channel_details = {
    1208596515115892816 : "fresh-non-new-grad",
    1186528627412705320 : "non-new-grad-jobs",
    1210065576920092702 : "fresh-new-grad",
    1186528561587298355 : "new-grad-jobs",
    1208597331503485009 : "startups",
    1215603773800452169 : "test-mit"
}



BOT_AUTH_TOKEN = os.getenv('BOTH_AUTH_TOKEN')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

def authenticate_with_g_sheets():

    gc = gspread.oauth(
        credentials_filename='./client_secrets3.json',
        authorized_user_filename='./storage.json'
    )
    
    spreadSheet = gc.open_by_key(SPREADSHEET_ID)

    # sheets = Sheets.from_files('./client_secrets3.json', './storage.json')
    # spreadSheet = sheets[SPREADSHEET_ID]
    worksheet = spreadSheet.get_worksheet(0)

    return worksheet

worksheet = authenticate_with_g_sheets()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await list_channels()


@client.event
async def on_message(message):
    fresh = False
    link = ''

    # if message.author == client.user:
    #     return

    if message.content.startswith('hello'):
        await message.channel.send('Hello!')
    
    if channel_details[message.channel.id].startswith('fresh'):
        fresh = True

    # Extract hyperlink
    links = re.findall(r'\bhttp[^\s]+',message.content)
    print(links)
    data = []
    for link in links:
        dataObj = {
            # "timestamp":message.created_at,
            "link":link,
            "type":channel_details[message.channel.id],
            "fresh":"Yes" if fresh else "No",
            "applied":"No",
            "referral":"No"
        }
        data.append(dataObj)
    await write_to_sheets(data)
    

async def list_channels():
    for guild in client.guilds:
        print(f'Channels in {guild.name}:')
        for channel in guild.channels:
            print(f' - {channel.name} (id: {channel.id})')
            # print(type(channel.id))


async def write_to_sheets(data):
    for item in data:
        worksheet.append_row(values=['',item["link"],item["type"],item["fresh"],item["applied"],item["referral"]])
    

client.run(BOT_AUTH_TOKEN)