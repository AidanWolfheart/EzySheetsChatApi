import json
from flask import Blueprint, Response, app

chat = Blueprint('chat', __name__)
chat.url_prefix = '/chat'
APPLICATION_JSON = 'application/json'


@chat.route('/')
def index():
    return Response(json.dumps("Hello, world"), mimetype=APPLICATION_JSON)


@chat.route('/upload', methods=['POST'])
def upload_item(item):
    return Response(json.dumps(item.token), mimetype=APPLICATION_JSON)
