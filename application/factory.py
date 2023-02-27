from flask import Flask
from application.api.chat import chat


def create_app():
    app = Flask(__name__)
    app.register_blueprint(chat, url_prefix=chat.url_prefix)

    return app
