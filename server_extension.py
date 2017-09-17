from __future__ import print_function
import apiclient
print(apiclient)
from flask import Flask
from flask import request
import calendar_helper

import json

import flask
import httplib2

from apiclient import discovery
from oauth2client import client

import datetime
import parsedatetime
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
CLIENT_SECRET_FILE = 'client_secret.json'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


app = flask.Flask(__name__)
credentials = get_credentials()

@app.route('/')
def index():
    return "yo this works"


@app.route('/add_event')
def add_event(credentials, input_string):
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    eventName, eventDateTimeString = input_string.split('!')
    startDateTimeString, endDateTimeString = eventDateTimeString.split('-')
    cal = parsedatetime.Calendar()
    start_time_struct = cal.parse(startDateTimeString)[0]
    end_time_struct = cal.parse(endDateTimeString)[0]
    startDateTime = datetime.datetime(*start_time_struct[:6])
    endDateTime = datetime.datetime(*end_time_struct[:6])
    
    event = {
      'summary' = eventName,
      'start' : {
        'dateTime': startDateTime.isoformat(),
        'timeZone': 'America/New_York',
      },
      'end' : {
        'dateTime': endDateTime.isoformat(),
        'timeZone': 'America/New_York',
      },
    }
    eventsResult = service.events().insert(
      calendarId='primary', body=event).execute()

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
    credentials = get_credentials()
    print(credentials)
    return calendar_helper.getEventList(credentials)

@app.route("/get_event_grid", methods=['GET'])
def get_event_grid():
    credentials = get_credentials()
    print(credentials)
    return calendar_helper.getEventGrid(credentials)
    pass

if __name__ == '__main__':
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug = False
    app.run()
