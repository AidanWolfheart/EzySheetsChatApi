from application.agent.load_tools import get_appscript_service, local_service
from application.tools.GoogleSheetsToolWrapper import GoogleSheetsToolWrapper, AppScriptToolWrapper

batch_update_test_reqeust = {
    "requests": [
        {
            "updateCells": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 0,
                    "endRowIndex": 5,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1
                },
                "rows": [
                    {
                        "values": [
                            {
                                "userEnteredValue": {
                                    "numberValue": 1
                                }
                            },
                            {
                                "userEnteredValue": {
                                    "numberValue": 2
                                }
                            },
                            {
                                "userEnteredValue": {
                                    "numberValue": 3
                                }
                            },
                            {
                                "userEnteredValue": {
                                    "numberValue": 4
                                }
                            },
                            {
                                "userEnteredValue": {
                                    "numberValue": 5
                                }
                            }
                        ]
                    }
                ],
                "fields": "userEnteredValue"
            }
        }
    ]
}

batch_update_test_reqeust1 = {
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

create_reqeust = {
    "properties": {
        "title": "my_test1"
    }
}

test_reqeust_2 = {
    "requests": [
        {
            "repeatCell": {
                "range": {
                    "startRowIndex": 0,
                    "endRowIndex": 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {
                            "red": 1,
                            "green": 1,
                            "blue": 0
                        }
                    }
                },
                "fields": "userEnteredFormat.backgroundColor",
                "condition": {
                    "type": "NUMBER_GREATER",
                    "values": [
                        {
                            "userEnteredValue": "3"
                        }
                    ]
                }
            }
        }
    ]
}


def init():
    service = local_service()
    return AppScriptToolWrapper(service=service)


def call_deploy_script(tool):
    scriptId = "1Ws462FLVENvSLb5JyOwS0ehdWfembe8n1YDxkTC1W_PKiMsAm92CFiDk"
    tool.deploy_script(scriptId)

def call_run_script(tool):
    scriptId = "1Ws462FLVENvSLb5JyOwS0ehdWfembe8n1YDxkTC1W_PKiMsAm92CFiDk"
    run_request = "createTable"
    tool.run_script(scriptId, run_request)


if __name__ == "__main__":
    # # run from root dir and run `python3 -m application.local_test`
    tool = init()
    # sheets = GoogleSheetsToolWrapper(service=service)
    # # sheets.create(create_request)
    # # sheets.batch_update_values('1fckx6R1uHS0si04wT54U354gE_oUReZJLVTygG8-uzE', batch_update_value_request)
    # your_sheetid = '1fckx6R1uHS0si04wT54U354gE_oUReZJLVTygG8-uzE'
    #
    # # Test
    # sheets.batch_update_values(your_sheetid, test_reqeust_2)
    # # sheets.create(create_reqeust)

    request = '''function highlightFirstRow() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var range = sheet.getDataRange();
  var values = range.getValues();
  for (var i = 0; i < values[0].length; i++) {
    if (values[0][i] > 3) {
      sheet.getRange(1, i+1).setBackground("yellow");
    }
  }
}
'''
    # scriptId = "1Ca_cZBxopuL9irK-Y0iCdnO9fUPxJMcm14qmLiVxUK4RRdmvC0Ug1lhE"
    # script_tool = GoogleSheetsToolWrapper1(service=service)
    # script_tool.update_script(scriptId, request)
    call_deploy_script(tool)
    #call_run_script(tool)
