from flask import Flask
from flask import request
import calendar_helper

import json

import flask
import httplib2

from apiclient import discovery
#python_client = __import__("google-api-python-client")
from oauth2client import client

import datetime


app = flask.Flask(__name__)
app.secret_key = "secret_key"


@app.route('/')
def index():
    return "yo this works"

def checkCredentials():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        service = discovery.build('calendar', 'v3', credentials=credentials)
    return credentials


@app.route('/add_event')
def add_event():
    credentials = checkCredentials()
    service = discovery.build('calendar', 'v3', credentials=credentials)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    return "done"

@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
    'client_secret.json',
    scope='https://www.googleapis.com/auth/calendar.readonly',
    redirect_uri='https://flask-extension-server.herokuapp.com/oauth2callback')
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('index'))



@app.route("/get_event_list", methods=['GET'])
def get_event_list():
    credentials = checkCredentials()
    print credentials
    return calendar_helper.getEventList(credentials)

@app.route("/get_event_grid", methods=['GET'])
def get_event_grid():
    pass

if __name__ == '__main__':
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug = False
    app.run()
