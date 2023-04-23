from __future__ import print_function

import flask
import json
import logging
from langchain.tools import BaseTool
from application.tools.GoogleSheetsToolWrapper import GoogleSheetsToolWrapper, AppScriptToolWrapper

sample_spreadsheet_id = '1fckx6R1uHS0si04wT54U354gE_oUReZJLVTygG8-uzE'
logging.getLogger('gunicorn.error')

scriptId = "1Ws462FLVENvSLb5JyOwS0ehdWfembe8n1YDxkTC1W_PKiMsAm92CFiDk"
deploymentId = "AKfycbxLdKTwSW2kTG8JEwqVT2Ju4EqSJDFDcJG9QOVj48pD03x-z5rPZq57fzzf_jijKn4K"


def get_session_script_id():
    return flask.session['script_id'] if 'script_id' in flask.session else ''

class GoogleSheetsScriptBaseTool(BaseTool):
    def sanitize_json(self, input_json_string):
        input_json_string = input_json_string.replace("```", "")
        return input_json_string

class AppScriptCreateScriptTool(GoogleSheetsScriptBaseTool):
    """Tool for executing the Google Sheets App Script Create method. Creates a new script"""

    name = "Google Sheets App Script Create method."
    description = (
        "A wrapper around Google Sheets App Script."
        "Useful for when you need to create a new App Script script"
        "Input should be a Script Name"
    )

    api_wrapper: AppScriptToolWrapper

    def _run(self, action_input: str) -> str:
        "Use the tool."
        return self.api_wrapper.create_script(sample_spreadsheet_id, self.sanitize_json(action_input))

    async def _arun(self, input: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Google Sheets run does not support async")


class AppScriptUpdateTool(GoogleSheetsScriptBaseTool):
    """Tool for updating the Google Sheets App Script script."""

    name = "Google Sheets App Script Update method."
    description = (
        "A wrapper around Google Sheets App Script."
        "Useful for when you need to Update the Google Sheets App Script script."
        "Input should be a function for App Script"
    )

    api_wrapper: AppScriptToolWrapper

    def _run(self, action_input: str) -> str:
        "Use the tool"
        logging.info(f"Google Sheet tool, action input: {action_input}\n")
        return self.api_wrapper.update_script(get_session_script_id(), self.sanitize_json(action_input))

    async def _arun(self, input: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Google Sheets run does not support async")


class AppScriptRunScriptTool(GoogleSheetsScriptBaseTool):
    """Tool for running Google Sheets App Script Run method."""

    name = "Google Sheets App Script Run method"
    description = (
        "A wrapper around Google Sheets App Script."
        "Useful for when you need to Run the Google Sheets App Script script."
        "Input should be a function name"

    )

    api_wrapper: AppScriptToolWrapper

    def _run(self, action_input: str) -> str:
        "Use the tool"
        return self.api_wrapper.run_script(deploymentId, self.sanitize_json(action_input))

    async def _arun(self, input: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Google Sheets run does not support async")

# =================== ===================

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