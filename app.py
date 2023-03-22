import os

from pydantic.datetime_parse import timedelta

from application.factory import create_app
from flask_cors import CORS

# TODO remove this
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = create_app()

