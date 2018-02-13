
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scopes = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name('phicops-b08565115ee3.json',scopes)

client = gspread.authorize(creds)

sheet = client.open('servicesheets').sheet1

print(sheet.cell(1,1))
