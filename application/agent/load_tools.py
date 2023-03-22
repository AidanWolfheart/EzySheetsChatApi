import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from application.tools.GoogleSheetsTool import GoogleSheetsBatchUpdateTool, GoogleSheetsCreateTool, GoogleSheetsGetTool, \
    GoogleSheetsValuesBatchUpdateTool
from application.tools.GoogleSheetsToolWrapper import GoogleSheetsToolWrapper

dirname = os.path.dirname(__file__)
client_secrets_filename = os.path.join(dirname, './client_secrets.json')
token_filename = os.path.join(dirname, './token.json')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_filename, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_filename, 'w') as token:
            token.write(creds.to_json())
    return build('sheets', 'v4', credentials=creds)


def load_tools():
    tools = []

    service = get_service()
    tools.append(GoogleSheetsBatchUpdateTool(api_wrapper=GoogleSheetsToolWrapper(service=service)))
    tools.append(GoogleSheetsCreateTool(api_wrapper=GoogleSheetsToolWrapper(service=service)))
    tools.append(GoogleSheetsGetTool(api_wrapper=GoogleSheetsToolWrapper(service=service)))
    tools.append(GoogleSheetsValuesBatchUpdateTool(api_wrapper=GoogleSheetsToolWrapper(service=service)))
    return tools
