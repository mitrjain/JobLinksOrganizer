FROM python:3.9.18-alpine3.19

WORKDIR /docker-bot

COPY mit-bot.py ./
COPY requirements.txt ./
COPY client_secrets* ./
COPY storage.json ./

RUN pip install -r requirements.txt

CMD ["python", "mit-bot.py"]