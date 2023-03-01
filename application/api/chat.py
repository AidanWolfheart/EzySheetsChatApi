import json
from flask import Blueprint, Response, request

chat = Blueprint('chat', __name__)
chat.url_prefix = '/chat'
APPLICATION_JSON = 'application/json'


@chat.route('/')
def index():
    return Response(json.dumps("Hello, world"), mimetype=APPLICATION_JSON)


@chat.route('/send-auth', methods=['POST'])
def send_auth():
    google_auth = request.get_json()
    return Response(json.dumps(google_auth), mimetype=APPLICATION_JSON)
