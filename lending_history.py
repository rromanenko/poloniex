#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 02:31:42 2017

@author: romanromanenko
"""

# Script that gets all my lending history and sums up all the earnings

import requests
import time
import hmac
import hashlib
import json
import urllib

from polo_config import *

import datetime
s = "29/03/2018"
start_time = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())
e = "20/07/2018"
end_time = time.mktime(datetime.datetime.strptime(e, "%d/%m/%Y").timetuple())
#end_time = int(time.time()) # время окончания - текущее

req = {'command': 'returnLendingHistory',
       'nonce': str(int(time.time())),
#       'account': 'all',
       'start': start_time,
       'end': end_time,
       'limit': 10000
       } 

post_data = urllib.parse.urlencode(req).encode('utf-8')
hmac_key = secret.encode('utf-8')

sign = hmac.new(hmac_key, post_data, hashlib.sha512)
sign = sign.hexdigest()

headers = { 'Content-type': 'application/x-www-form-urlencoded',
            'Sign': sign,
            'Key': key }

# getting my lending history
res = requests.post('https://poloniex.com/tradingApi', data=post_data, headers=headers).json()

#calculate all my earnings from lending
sum = 0
n = 0
for i in res:
    sum += float(i['earned'])
    n += 1

print(round(sum,8), n)