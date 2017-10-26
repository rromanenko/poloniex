#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 22:27:50 2017

@author: romanromanenko
"""

import requests
import time
import hmac
import hashlib
import json
import urllib
from polo_config import *

#import for SMTP
import smtplib

# getting daily stats
ticker = requests.get("https://poloniex.com/public?command=returnTicker").json()
polo_output = {}

#reduce daily stats to only needed ones and add them to the global output dictionary
for i in ticker['USDT_BTC']:
    if i in ('last', 'high24hr', 'low24hr'):
        polo_output[i] = ticker['USDT_BTC'][i]

# getting my account balance
req = {'command': 'returnCompleteBalances',
       'nonce': str(int(time.time())),
       'account': 'all' }

post_data = urllib.parse.urlencode(req).encode('utf-8')
hmac_key = secret.encode('utf-8')

sign = hmac.new(hmac_key, post_data, hashlib.sha512)
sign = sign.hexdigest()

headers = { 'Content-type': 'application/x-www-form-urlencoded',
            'Sign': sign,
            'Key': key }

res = requests.post('https://poloniex.com/tradingApi', data=post_data, headers=headers).json()

#add BTC balance details to the global output dictionary
for i in res['BTC']:
    polo_output[i] = res['BTC'][i]

# last_btc_value.txt file btcValue that we had during our previous check.
# if check it against the current btcValue and add the difference (if any)
# to global output dictionary
# Otherwise (if file not found, if file doesn't contain last btcValue, and if
# there is a difference between last and current btcValue), we write current btcValue
# into the file
rewrite_file_flag = False

try:
    last_btc_file = open("last_btc_value.txt", "r")
    last_btc_value_str = last_btc_file.readline().strip()

    try:
        last_btc_value = float(last_btc_value_str)
        btc_diff = round( float(polo_output["btcValue"]) - last_btc_value,8 )
        if btc_diff > 0:
            polo_output['earned BTC'] = '{0:.8f}'.format(btc_diff)
            polo_output['earned USD'] = round( btc_diff * int(float(polo_output['last'])),3 )
            rewrite_file_flag = True
        else:
            rewrite_file_flag = False
    except ValueError:
        rewrite_file_flag = True

except FileNotFoundError:
    rewrite_file_flag = True

if rewrite_file_flag:
    last_btc_file = open("last_btc_value.txt", "w")
    last_btc_file.write(polo_output["btcValue"])

last_btc_file.close()

# format resulted json and convert to str before sending
polo_output_str = str(json.dumps(polo_output, sort_keys=True, indent=4))

# send an email with all details
server = smtplib.SMTP('smtp.gmail.com', 587)
#server.ehlo()
server.starttls()

# Email details in config file

server.login(from_email, from_email_pass)

msg = "\r\n".join([
  "From: " + from_email,
  "To: " + to_email,
  "Subject: BTC at Polo today",
  "",
  polo_output_str
  ])

server.sendmail(from_email, to_email, msg)

server.quit()