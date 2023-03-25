from __future__ import print_function

import os.path
import traceback
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from pydantic import BaseModel
from googleapiclient import errors

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

create_request = {
    'properties': {
        'title': "EzySheets_test1"
    }
}

SHEET_ID = 0


batch_update_value_request = {
    "valueInputOption": "RAW",
    "data": [
        {
            "range": "Sheet1!A1:C3",
            "majorDimension": "ROWS",
            "values": [
                ["Name", "Age", "Gender"],
                ["John Doe", "32", "Male"],
                ["Jane Smith", "28", "Female"]
            ]
        }
    ]
}

dirname = os.path.dirname(__file__)
client_secrets_filename = os.path.join(dirname, '../agent/client_secrets.json')
token_filename = os.path.join(dirname, '../../.env/token.json')


class AppScriptToolWrapper(BaseModel):
    """Tool Wrapper for executing App Script Code"""

    service: Any

    name = "Google Sheets App Script"
    description = "Useful for executing Google Sheets App Script Methods."

    def create_script(self, request):

        body = {'title': request.strip()}

        try:
            response = self.service.projects().create(body=body).execute()
        except errors.HttpError as error:
            print(error.content)
            response = None
        return response

    def update_script(self, scriptId, request):
        print(f"---- request: {request}\n")
        body = {
            'files': [{
                'name': 'tool1',
                'type': 'SERVER_JS',
                'source': request.strip()
            }, {
                'name': 'appsscript',
                'type': 'JSON',
                'source': '''
                            {
                            "timeZone": "Asia/Almaty",
                            "exceptionLogging": "CLOUD"
                            }
                            '''.strip()
            }]
        }
        print("Updating script...")
        print(f"=========== \n scriptId: {scriptId} \n body: {body} \n ===========")
        try:
            response = self.service.projects().updateContent(
                body=body,
                scriptId=scriptId
            ).execute()
            result = "Update was successful!"
            print(result)
        except errors.HttpError as error:
            print("Encountered erroring while executing update: " + error.content)
            result = "Update was unsuccessful"
        return result

    def run_script(self, scriptId, request):
        try:
            response = self.service.scripts().run(scriptId=scriptId, body=request).execute()
        except errors.HttpError as error:
            print(error.content)
            response = None
        return response

class GoogleSheetsToolWrapper(BaseModel):
    """Tool for executing Google Sheets API Methods."""

    service: Any

    name = "Google Sheets"
    description = "Useful for executing Google Sheets API Methods"

    def create(self, request):
        try:
            print("Calling create with the following json: ")
            print(request)

            request = self.service.spreadsheets().create(body=request, fields='spreadsheetId')
            response = request.execute()
            print(f"Spreadsheet ID: {(response.get('spreadsheetId'))}")
        except HttpError as error:
            print(f"An error occurred: {error}")
            response = None
        return response

    def batch_update(self, spreadsheet_id, request):
        try:
            print("Calling batch_update with the following json: ")
            print(request)

            request = self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=request)
            response = request.execute()
        except Exception as error:
            print(f"An error occurred: {traceback.print_exc()}")
            response = None
        return response

    def batch_update_values(self, spreadsheet_id, request):
        try:
            request = self.service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request)
            response = request.execute()
        except HttpError as error:
            print(f"An error occurred: {error}")
            response = None
        return response

    def get(self, spreadsheetId, ranges):
        try:
            print("Calling get with the following range: ")
            print(ranges)

            request = self.service.spreadsheets().get(spreadsheetId=spreadsheetId, ranges=ranges)
            response = request.execute()
        except HttpError as error:
            print(f"An error occurred: {error}")
            response = None
        return response

    def batch_clear_by_data_filter(self, spreadsheetId, request):
        try:
            request = self.service.spreasheets().batchClearByDataFilter(spreadsheetId=spreadsheetId, body=request)
            response = request.execute()
        except HttpError as error:
            print(f"An error occurred: {error}")
            response = None
        return response

    def _run(self, spreadsheetId: str, request: str) -> str:
        """This function should be a wrapper for all the functions above"""
        action = {
            'sheet': self.get_service(),
            'create': self.create(spreadsheetId=spreadsheetId, request=request),
            'update': self.batch_update(spreadsheet_id=spreadsheetId, request=request),
            'get': self.get(spreadsheetId=spreadsheetId, request=request),
            'clear': self.batch_clear_by_data_filter(spreadsheetId=spreadsheetId, request=request)
        }

        response_as_json = json.dumps(action)
        return response_as_json

    async def _arun(self, range_name: str) -> str:
        """Use the tool asynchronously to retrieve data from a Google Sheets spreadsheet."""
        raise NotImplementedError("GoogleSheetsTool does not support async")


batch_update_request = '''
{
    "requests": [
        {
            "appendDimension": {
                "sheetId": SHEET_ID,
                "dimension": "COLUMNS",
                "length": 1
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": SHEET_ID,
                    "startRowIndex": 0,
                    "endRowIndex": 3,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1
                },
                "cell": {
                    "userEnteredValue": {
                        "numberValue": 1
                    }
                },
                "fields": "userEnteredValue"
            }
        }
    ]
}
'''

test_json = '''
```
{
  "requests": [
    {
      "repeatCell": {
        "range": {
          "sheetId": 0,
          "startRowIndex": 0,
          "endRowIndex": 5,
          "startColumnIndex": 0,
          "endColumnIndex": 1
        },
        "cell": {
          "userEnteredValue": {
            "numberValue": 1
          }
        },
        "fields": "userEnteredValue"
      }
    }
  ]
}
```
'''

create_reqeust = '''{
  "properties": {
    "title": "My Spreadsheet"
  },
  "sheets": [
    {
      "properties": {
        "title": "Sheet1"
      }
    }
  ]
}
'''

if __name__ == "__main__":
    service = get_service()
    sheets = GoogleSheetsToolWrapper(service)
    # sheets.create(create_request)
    # sheets.batch_update_values('1fckx6R1uHS0si04wT54U354gE_oUReZJLVTygG8-uzE', batch_update_value_request)
    your_sheetid = '1fckx6R1uHS0si04wT54U354gE_oUReZJLVTygG8-uzE'
    # sheets.batch_update(your_sheetid, test_json)
    sheets.create(test_json)
