from gsheets import Sheets
sheets = Sheets.from_files('./client_secrets3.json', './storage.json')
sheets  #doctest: +ELLIPSIS