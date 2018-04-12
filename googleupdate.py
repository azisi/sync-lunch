#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

from settings import *

import datetime
from datetime import datetime
import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

import sys
import requests,re

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

def deleteevents(edate):

    ## get all other events in the same day and delete them
    tMax = datetime.strptime(edate,'%d/%m/%Y').strftime('%Y-%m-%d')+'T23:59:59Z'
    tMin = datetime.strptime(edate,'%d/%m/%Y').strftime('%Y-%m-%d')+'T00:00:00Z'
    page_token = None
    while True:
        print u'Searching for events between %s and %s' % (tMin,tMax)
        events = service.events().list(calendarId='primary', timeMax=tMax, timeMin=tMin, pageToken=page_token).execute()
        for event in events['items']:
            print u'Deleting event %s %s' % (event['start'], event['summary'])
            service.events().delete(calendarId='primary', eventId=event['id']).execute()
        page_token = events.get('nextPageToken')
        if not page_token:
            break

def insertevent(edate,esummary):

    ## insert the new event
    date_isoformat = datetime.strptime(edate,'%d/%m/%Y').strftime('%Y-%m-%d')
    event = {
        'summary': esummary,
        'start': {
            'date': date_isoformat,
            'timeZone': 'Europe/Athens',
        },
        'end': {
            'date': date_isoformat,
            'timeZone': 'Europe/Athens',
        },
    }

    print u'Inserting event %s %s' % (event['start'], event['summary'])
    event = service.events().insert(calendarId='primary',body=event).execute()
    print u'Event created: %s' % (event.get('htmlLink'))

scopes = ['https://www.googleapis.com/auth/calendar']
credentials = ServiceAccountCredentials.from_json_keyfile_name( CREDENTIAL_JSON_FILE, scopes=scopes)

'''
            <tr style="background: lightgray">

                <td>16/10/2017</td>
                <td>42</td>
                <td>ΔΕΥΤΕΡΑ</td>
                <td>4116</td>
                <td>ΚΟΤΟΠΟΥΛΟ ΚΕΦΤΕΔΑΚΙΑ ΜΕ ΡΥΖΙ</td>
                <td></td>
            </tr>
'''

content=sys.stdin.readlines()
orders = {}
keys = [u'date',u'week',u'day',u'code',u'order',u'remarks']
curdate = None
index = 0
for line in content:
    m = re.match(r'^.*<td>(?P<value>\d+\/\d+\/\d+)</td>.*',line)
    if m != None:
        print u'Found date %s' % (m.group('value'))
        curdate = m.group('value')
        orders[curdate] = {}
        index = 0
    else:
        m = re.match(r'^.*<td>(?P<value>.*)</td>.*',line)
        if m != None:
            index += 1
            ##print u'Found %s %s' % (keys[index],m.group('value'))
            s = m.group('value').decode('utf8')
            print u'Found %s %s' % (keys[index],s)
            orders[curdate][keys[index]] = s

http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)

for key,value in orders.iteritems():
    deleteevents(key)
    insertevent(key,value['order'])
    
