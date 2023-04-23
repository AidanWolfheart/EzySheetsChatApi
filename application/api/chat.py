import flask
import google
import google_auth_oauthlib
from google.auth.transport import requests

from application.constants.constants import CLIENT_SECRETS_FILE, SCOPES, WORKING_URL, PROTOCOL
from application.handlers.message_handler import MessageHandler
from flask import Blueprint, Response, request, jsonify
import json
import traceback
import logging

from application.shared.helpers import credentials_to_dict

chat = Blueprint('chat', __name__)
chat.url_prefix = '/chat'
APPLICATION_JSON = 'application/json'

message_handler = MessageHandler()
logging.getLogger('gunicorn.error')


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
        if 'credentials' not in flask.session:
            return flask.redirect('authorize')

        reqeust_body = request.get_json()
        userid = reqeust_body.get('userid')
        message = reqeust_body.get('message')

        logging.info(f'userid: {userid}, msg={message}, body: {reqeust_body}')
        response_string = message_handler.handle_message(userid, message)
        return Response(json.dumps(response_string), mimetype=APPLICATION_JSON)
    except Exception:
        error = f'Encountered error: {traceback.format_exc()})'
        logging.error(error)
        return Response(json.dumps("Error has occurred. Please try again."), mimetype=APPLICATION_JSON)


@chat.route('/authorize', methods=['GET'])
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = flask.url_for('chat.oauth2callback', _external=True, _scheme=PROTOCOL)

    if 'state' in flask.session and 'credentials' in flask.session:
        return jsonify({"url": WORKING_URL})

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state

    flask.session.modified = True

    return jsonify({"url": authorization_url})


@chat.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', WORKING_URL)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@chat.route('/oauth2callback', methods=['GET'])
def oauth2callback():
    if request.method == "OPTIONS":  # CORS preflight
        return 200

    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = request.args.get('state')

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('chat.oauth2callback', _external=True, _scheme=PROTOCOL)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)
    flask.session['refresh_token'] = credentials.refresh_token

    flask.session.modified = True

    response = flask.redirect(WORKING_URL)
    return response


@chat.route('/signed-in', methods=['GET'])
def signed_in():
    credentials_exist = False

    if 'credentials' in flask.session:
        credentials_exist = True

    return jsonify({"creds": credentials_exist})

@chat.route('/set-active-script-id', methods=['POST'])
def set_active_script_id():
    script_id = request.get_json().get('script_id')

    flask.session['script_id'] = script_id
    return Response(json.dumps("Set active script to "+script_id), mimetype=APPLICATION_JSON)

@chat.route('/get-active-script-id', methods=['GET'])
def get_active_script_id():
    active_script_id = ''

    if 'script_id' in flask.session:
        active_script_id = flask.session['script_id']

    return jsonify({'scriptId':active_script_id})


@chat.route('/revoke', methods=['GET'])
def revoke():
    if 'credentials' not in flask.session:
        return ('You need to <a href="/authorize">authorize</a> before ' +
                'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    revoke = requests.post('https://oauth2.googleapis.com/revoke',
                           params={'token': credentials.token},
                           headers={'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return ('Credentials successfully revoked.')
    else:
        return ('An error occurred.')
