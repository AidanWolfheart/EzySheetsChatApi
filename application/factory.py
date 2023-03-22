from flask import Flask
from flask_cors import CORS
from flask_session import Session

import redis

from application.api.chat import chat


def create_app():
    app = Flask(__name__)
    app.register_blueprint(chat, url_prefix=chat.url_prefix)

    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'redis'
    app.config['ORIGINS'] = 'http://localhost:4200'
    #CORS(app, supports_credentials=True)
    CORS(app, resources={r'/chat/*': {'origins': '*'}})
    app.config['SESSION_PERMANENT'] = True
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = "None"

    Session(app)

    return app
