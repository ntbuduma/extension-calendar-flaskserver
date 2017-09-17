from flask import Flask
from flask import request
import calendar_helper

import json

import flask
import httplib2

from apiclient import discovery
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
        http_auth = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http_auth)
    return credentials


@app.route('/add_event')
def add_event():
    credentials = checkCredentials()
    return calendar_helper.getEventList(credentials)

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
    return calendar_helper.getEventList(credentials)

@app.route("/get_event_grid", methods=['GET'])
def get_event_grid():
    pass

if __name__ == '__main__':
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug = False
    app.run()

