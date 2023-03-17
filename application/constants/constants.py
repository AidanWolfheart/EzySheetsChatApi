import json
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../../config.json')

f = open(filename)
data = json.load(f)

OPENAI_API_KEY = data['OPENAI_API_KEY']

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

CLIENT_SECRETS_FILE = os.path.join(dirname, './client_secrets.json')

TOKEN_FILE = os.path.join(dirname, './token.json')