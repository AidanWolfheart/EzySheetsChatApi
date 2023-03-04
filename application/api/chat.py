from application.handlers.message_handler import MessageHandler
from flask import Blueprint, Response, request
import json
import traceback

chat = Blueprint('chat', __name__)
chat.url_prefix = '/chat'
APPLICATION_JSON = 'application/json'

message_handler = MessageHandler()

@chat.route('/')
def index():
    return Response(json.dumps("Hello, world"), mimetype=APPLICATION_JSON)


@chat.route('/send-auth', methods=['POST'])
def send_auth():
    google_auth = request.get_json()
    return Response(json.dumps(google_auth), mimetype=APPLICATION_JSON)


@chat.route('/conversation', methods=['POST'])
def conversation():
    try:
        reqeust_body = request.get_json()
        userid = reqeust_body.get('userid')
        message = reqeust_body.get('message')
        print(f'userid: {userid}, msg={message}, body: {reqeust_body}')
        response_string = message_handler.handle_message(userid, message)
        return Response(json.dumps(response_string), mimetype=APPLICATION_JSON)
    except Exception:
        error = f'Encountered error: {traceback.format_exc()})'
        print(error)
        return Response(json.dumps(error), mimetype=APPLICATION_JSON)
