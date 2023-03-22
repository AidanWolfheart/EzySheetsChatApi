from application.agent.load_tools import get_service
from application.tools.GoogleSheetsToolWrapper import GoogleSheetsToolWrapper

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


if __name__ == "__main__":
    # run from root dir and run `python3 -m application.local_test`
    service = get_service()
    sheets = GoogleSheetsToolWrapper(service=service)
    # sheets.create(create_request)
    # sheets.batch_update_values('1fckx6R1uHS0si04wT54U354gE_oUReZJLVTygG8-uzE', batch_update_value_request)
    your_sheetid = '1fckx6R1uHS0si04wT54U354gE_oUReZJLVTygG8-uzE'

    # Test
    sheets.batch_update_values(your_sheetid, test_reqeust_2)
    # sheets.create(create_reqeust)

