# EzySheeysChatAPI
This is a project that provides the API that allows you to chat with an AI

## Setup
Put necessary keys in the `config.json` file

## How start project
Run the following command to start the flask backend
```
flask run
```

## Manually Testing the API
```
# Run the following command back to back. Should give end result of: 105
curl -X POST http://127.0.0.1:5000/chat/conversation -H 'Content-Type: application/json' -d '{"userid":"1","message":"Whats 10 times 10"}'
curl -X POST http://127.0.0.1:5000/chat/conversation -H 'Content-Type: application/json' -d '{"userid":"1","message":"and plus 5"}'
curl -X POST http://127.0.0.1:5000/chat/conversation -H 'Content-Type: application/json' -d '{"userid":"1","message":"Write 1 to 5 to cell A1 to A5 in my google sheet with sheetid=0"}'
```