import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from application.tools.GoogleSheetsTool import GoogleSheetsBatchUpdateTool, GoogleSheetsCreateTool, GoogleSheetsGetTool, \
    GoogleSheetsValuesBatchUpdateTool, AppScriptUpdateTool, AppScriptRunScriptTool
from application.tools.GoogleSheetsToolWrapper import GoogleSheetsToolWrapper, AppScriptToolWrapper

dirname = os.path.dirname(__file__)
client_secrets_filename = os.path.join(dirname, '../../.env/client_secrets.json')
token_filename = os.path.join(dirname, '../../.env/token.json')

SCOPES = ['https://www.googleapis.com/auth/script.projects']


def get_service():
    creds = None
    if os.path.exists('../../.env/token.json'):
        creds = Credentials.from_authorized_user_file('../../.env/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_filename, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_filename, 'w') as token:
            token.write(creds.to_json())
    return build('script', 'v1', credentials=creds)


def load_tools():
    tools = []

    service = get_service()
    tools.append(AppScriptUpdateTool(api_wrapper=AppScriptToolWrapper(service=service)))
    tools.append(AppScriptRunScriptTool(api_wrapper=AppScriptToolWrapper(service=service)))
    # tools.append(GoogleSheetsCreateTool(api_wrapper=GoogleSheetsToolWrapper(service=service)))
    # tools.append(GoogleSheetsGetTool(api_wrapper=GoogleSheetsToolWrapper(service=service)))
    # tools.append(GoogleSheetsValuesBatchUpdateTool(api_wrapper=GoogleSheetsToolWrapper(service=service)))
    return tools
