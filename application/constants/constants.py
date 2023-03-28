import json
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../../.env/config.json')

f = open(filename)
data = json.load(f)

OPENAI_API_KEY = data['OPENAI_API_KEY']

SCOPES = ['https://www.googleapis.com/auth/drive.scripts',
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/script.projects',
          'https://www.googleapis.com/auth/script.processes',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/script.scriptapp',
          'https://www.googleapis.com/auth/script.external_request']


CLIENT_SECRETS_FILE = os.path.join(dirname, '../../.env/client_secrets.json')

TOKEN_FILE = os.path.join(dirname, '../../.env/token.json')