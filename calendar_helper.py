from __future__ import print_function
import httplib2
import os
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'chrome-calendar-extension'

def getTruncatedDateTime(dateTime):
    """ Truncates a dateTime to the most recent midnight
    """
    return dateTime.split('T')[0]+"T00:00:00Z"


def parseDateTimeString(dateTime):
    """ Returns a date and a time given the date time string
        The time could be an empty string
    """
    if len(dateTime.split('T')) == 2:
        date, time = dateTime.split('T')
    else:
        date, time = [dateTime, ""]


    date = date.split('-', 1)[1]
    return date, time

"""
def addEvent(credentials, ):
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    event = #TODO
    eventsResult = service.events().insert(
            calendarId='primary', body=event).execute()
"""

""" Compiles the next $num_events events in the calendar in 
    the format 
        NAME DATE TIME LOCATION
    """
def getEventList(credentials, num_events = 10):
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    output = {}
    for idx, event in enumerate(events):
        start = event['start'].get('dateTime', event['start'].get('date'))
        location = ""
        if 'location' in event.keys():
            location = event['location']
        print(event['summary'], parseDateTimeString(start)[0], parseDateTimeString(start)[1], location)
        output[idx] = {
                'name': event['summary'],
                'date': parseDateTimeString(start)[0],
                'time': parseDateTimeString(start)[1],
                'location': location,
            }
    print(json.dumps(output))
    return json.dumps(output)

def getEventGrid(credentials):
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    today = datetime.datetime.utcnow()
    nextweek = today + datetime.timedelta(days = 7)
    today = getTruncatedDateTime(today.isoformat())
    nextweek = getTruncatedDateTime(nextweek.isoformat())

    eventsResult = service.events().list(
        calendarId='primary', timeMin=today, timeMax=nextweek, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    output = {}
    for idx, event in enumerate(events):
        start = event['start'].get('dateTime', event['start'].get('date'))
        location = ""
        if 'location' in event.keys():
            location = event['location']
        print(event['summary'], parseDateTimeString(start)[0], parseDateTimeString(start)[1], location)
        output[idx] = {
                'name': event['summary'],
                'date': parseDateTimeString(start)[0],
                'time': parseDateTimeString(start)[1],
                'location': location,
        }

