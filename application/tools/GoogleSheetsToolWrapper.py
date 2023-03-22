from __future__ import print_function

import os.path
import traceback
from typing import Any

import flask
import google
import google_auth_oauthlib
import httplib2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from pydantic import BaseModel
from oauth2client import client

from application.shared.helpers import credentials_to_dict

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

class GoogleSheetsToolWrapper(BaseModel):
    """Tool for executing Google Sheets API Methods."""

    name = "Google Sheets"
    description = "Useful for executing Google Sheets API Methods"
    creds: Any
    service: Any

    def __init__(self):
        super().__init__()
        self.get_service()

    def get_service(self):
        # Load credentials from the session.
        self.creds = google.oauth2.credentials.Credentials(
            **flask.session['credentials'])

        self.service = build('sheets', 'v4', credentials=self.creds)
        flask.session['credentials'] = credentials_to_dict(self.creds)

    def create(self, request):
        try:
            request = self.service.spreadsheets().create(body=request, fields='spreadsheetId')
            response = request.execute()
            print(f"Spreadsheet ID: {(response.get('spreadsheetId'))}")
        except HttpError as error:
            print(f"An error occurred: {error}")
            response = None
        return response

    def batch_update(self, spreadsheetId, request):
        try:
            print("Using batch_update API")
            print("Request: ")
            request = request.replace("```", "")
            print(request)
            request = json.loads(request)
            request = self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=request)
            response = request.execute()
        except Exception as error:
            print(f"An error occurred: {traceback.print_exc()}")
            response = None
        return response

    def batch_update_values(self, spreadsheetId, request):
        try:
            request = self.service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body=request)
            response = request.execute()
        except HttpError as error:
            print(f"An error occurred: {error}")
            response = None
        return response

    def get(self, spreadsheetId):
        try:
            request = self.service.spreadsheets().get(spreadsheetId=spreadsheetId)
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
            'update': self.batch_update(spreadsheetId=spreadsheetId, request=request),
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

if __name__ == "__main__":
    sheets = GoogleSheetsToolWrapper()
    # sheets.create(create_request)
    # sheets.batch_update_values('1fckx6R1uHS0si04wT54U354gE_oUReZJLVTygG8-uzE', batch_update_value_request)
    your_sheetid = '1fckx6R1uHS0si04wT54U354gE_oUReZJLVTygG8-uzE'
    sheets.batch_update(your_sheetid, test_json)
