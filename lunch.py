#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import *

import requests
import re
from datetime import *

'''
Login to the site
'''
def login():
    session = requests.Session()
    r = session.get(URL_LOGIN)
    content =  r.text.encode('utf-8')
    line=content.replace('\n','')
    '''
    Get the hidden input param __RequestVerificationToken
    '''
    m = re.match('.*RequestVerificationToken\" type=\"hidden\" value=\"(?P<token>\S+)\".*',line)
    token=m.group('token')
    payload={'Username':USERNAME,'Password':PASSWORD,'RememberMe':'false','__RequestVerificationToken':token}
    r=session.post(URL_LOGIN,data=payload)
    print 'Logging to the site'
    print 'Got response code %s' % (r.status_code)
    return session

'''
Week start datetime
'''
def week_start(d):
    while d.isoweekday() != 1: ## while not Monday
        d = d - timedelta(days=1)
    return d

'''
Week end datetime
'''
def week_end(d): 
    if d.isoweekday() == 6: ## If it's Saturday -1 is Friday
        d = d - timedelta(days=1)
    elif d.isoweekday() == 7: ## if it's Sunday -2 is Friday
        d = d - timedelta(days=2)
    else:
        while d.isoweekday() != 5: ## +1 until it is Friday
            d = d + timedelta(days=1)
    return d

'''
Get the food order for the current week
'''
def getmenu(session,d):
    
    fromdate = week_start(d)
    enddate = week_end(d)

    url = URL_MENU.format(fromdate.strftime('%d/%m/%Y'),enddate.strftime('%d/%m/%Y'))
    r = session.get(url)
    return r.text

print getmenu(login(),datetime.now()).encode('utf-8')
print getmenu(login(),datetime.now()+timedelta(days=7)).encode('utf-8')
