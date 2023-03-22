from __future__ import print_function

import os.path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from langchain.tools import BaseTool

from application.tools.GoogleSheetsToolWrapper import GoogleSheetsToolWrapper

sample_spreadsheet_id = '1fckx6R1uHS0si04wT54U354gE_oUReZJLVTygG8-uzE'

class GoogleSheetsBaseTool(BaseTool):
    def sanitize_json(self, input_json_string):
        input_json_string = input_json_string.replace("```", "")
        json_request = json.loads(input_json_string)
        return json_request

class GoogleSheetsBatchUpdateTool(GoogleSheetsBaseTool):
    """Tool for executing the Google Sheets Batch Update API."""

    name = "Google Sheets Batch Update API"
    description = (
        "A wrapper around Google Sheets. "
        "Useful for when you need to use the Google Sheets Batch Update API. "
        "Input should be a json request."
    )

    api_wrapper: GoogleSheetsToolWrapper

    def _run(self, action_input: str) -> str:
        """Use the tool."""
        return self.api_wrapper.batch_update(sample_spreadsheet_id,
                                             self.sanitize_json(action_input))

    async def _arun(self, input: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Google Sheets run does not support async")


class GoogleSheetsCreateTool(GoogleSheetsBaseTool):
    """Tool for executing the Google Sheets Create API. Creates a spreadsheet, returning the newly created spreadsheet"""

    name = "Google Sheets Create API"
    description = (
        "A wrapper around Google Sheets. "
        "Useful for when you need to use the Google Sheets Create API. "
        "Input should be a json request."
    )

    api_wrapper: GoogleSheetsToolWrapper

    def _run(self, action_input: str) -> str:
        """Use the tool."""
        return self.api_wrapper.create(self.sanitize_json(action_input))

    async def _arun(self, input: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Google Sheets run does not support async")


class GoogleSheetsGetTool(GoogleSheetsBaseTool):
    """Tool for executing the Google Sheets Get API. Gets the values inside a spreadsheet"""

    name = "Google Sheets Get API"
    description = (
        "A wrapper around Google Sheets. "
        "Useful for when you need to use the Google Sheets Get API. "
        "Input should be a json request"
    )

    api_wrapper: GoogleSheetsToolWrapper

    def _run(self, action_input: str) -> str:
        """Use the tool."""
        # - Spreadsheet ID: 0
        # - Range: A1:Z1000
        key_values = action_input.split('\n')
        sheetid = key_values[0].split('Spreadsheet ID: ')[1]
        cell_ranges = key_values[1].split('Range: ')[1]
        return self.api_wrapper.get(sample_spreadsheet_id, cell_ranges)

    async def _arun(self, input: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Google Sheets run does not support async")


class GoogleSheetsValuesBatchUpdateTool(GoogleSheetsBaseTool):
    """Tool for executing the Google Sheets Get API. Gets the values inside a spreadsheet"""

    name = "Google Sheets Spreadsheets.Values.BatchUpdate API"
    description = (
        "A wrapper around Google Sheets. "
        "Useful for when you need to use the Google Sheets Spreadsheets.Values.BatchUpdate API. "
        "Input should be a json request"
    )

    api_wrapper: GoogleSheetsToolWrapper

    def _run(self, action_input: str) -> str:
        """Use the tool."""
        return self.api_wrapper.batch_update_values(sample_spreadsheet_id, self.sanitize_json(action_input))

    async def _arun(self, input: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Google Sheets run does not support async")



