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


class GoogleSheetsBatchUpdateTool(BaseTool):
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
        return self.api_wrapper.batch_update('1fckx6R1uHS0si04wT54U354gE_oUReZJLVTygG8-uzE', action_input)

    async def _arun(self, input: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Google Sheets run does not support async")