import os

from pydantic.datetime_parse import timedelta

from application.factory import create_app
from flask_cors import CORS

# TODO remove this
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = create_app()
# Quick test configuration. Please use proper Flask configuration options
# in production settings, and use a separate file or environment variables
# to manage the secret key!
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
CORS(app, supports_credentials=True)
