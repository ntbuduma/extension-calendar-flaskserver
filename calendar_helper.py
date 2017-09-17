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

def getTimeFromTimeString(timeString):
    """ Given a time string of form AB:XX:XX-CD:XX:XX, 
        return the integer pair (AB,CD)
    """
    time = time.split('-')[0].rsplit(':',1)[0]

    startTimeString, endTimeString = timeString.split('-')
    print(startTimeString)
    print(endTimeString)
    startTime = startTimeString.split(':')[0].rsplit(':',1)
    endTime = endTimeString.split(':')[0]
    return [int(startTime), int(endTime)]

def getDateFromDateString(dateString):
    """ Given a date string of form MM-DD return the date
    """
    eventYear, eventMonth, eventDay = dateString.split('-')
    eventDate = datetime.date(year = int(eventYear), month = int(eventMonth), day = int(eventDay))
    return eventDate

def getDayFromEventString(dayString):
    """ Returns the number of days away the event with daystring
    $dayString is
    """
    eventDate = getDateFromDateString(dayString)
    nowDate = datetime.datetime.now().date()
    days = (eventDate-nowDate).days
    return days
 
def getDayAndIntervalFromStartAndEnd(start, end):
    """ Given a date string from an event, figures out how many 
    days away from now it is and the interval
    """
    if len(start.split('T')) == 2:
        date, startTime = start.split('T')
        date.split('-', 1)[1]
        days = getDayFromEventString(date)
        startTime = int(startTime.split('-')[0].split(':')[0])
        endTime = int(end.split('T')[1].split('-')[0].split(':')[0])
        return True, days, startTime, endTime
    else:
        date = start.split('T')[0]
        date.split('-', 1)[1]
        days = getDayFromEventString(date)
        return False, days, 0, 0

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
        time = time.split('-')[0].rsplit(':',1)[0]
    else:
        date, time = [dateTime, ""]


    date = date.split('-', 1)[1]
    return date, time


def addEvent(credentials):
    pass
    """
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    event = #TODO
    eventsResult = service.events().insert(
            calendarId='primary', body=event).execute()
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
        end = event['end'].get('dateTime', event['end'].get('date'))

        startDate, startTime = parseDateTimeString(start)
        endDate, endTime = parseDateTimeString(end)
        
        location = ""
        if 'location' in event.keys():
            location = event['location']
        print(event['summary'], startDate, startTime, endTime, location)
        output[idx] = {
                'name': event['summary'],
                'date': startDate,
                'time': str(startTime)+'-'+str(endTime),
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

    output = np.chararray((7,24))
    output[:] = "empty"
    
    for idx, event in enumerate(events):
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))

        startDate, startTime = parseDateTimeString(start)
        endDate, endTime = parseDateTimeString(end)
        
        
        location = ""
        if 'location' in event.keys():
            location = event['location']
        print(event['summary'], startDate, startTime, endTime, location)
        mode, days, startHour, endHour = getDayAndIntervalFromStartAndEnd(start, end)

        for i in range(startHour, endHour):
            output[days][i] = 'k'

    return json.dumps({'data': list(output.flatten(1))})


