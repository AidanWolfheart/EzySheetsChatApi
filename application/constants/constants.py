import json
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../../.env/config.json')

f = open(filename)
data = json.load(f)

OPENAI_API_KEY = data['OPENAI_API_KEY']
WORKING_URL = data['WORKING_URL']
PROTOCOL = data['PROTOCOL']

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/script.projects']

CLIENT_SECRETS_FILE = os.path.join(dirname, '../../.env/client_secrets.json')

TOKEN_FILE = os.path.join(dirname, './token.json')

