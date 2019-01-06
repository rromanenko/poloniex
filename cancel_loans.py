#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 23:18:58 2018

@author: romanromanenko
"""

from poloniex_api import Poloniex
from polo_config import *
import datetime

my_polo = Poloniex(
  API_KEY = key_lend,
  API_SECRET = secret_lend)

my_open_offers = my_polo.returnOpenLoanOffers()

# my_open_offers = {'BTC': [{'id': 1053294329, 'rate': '0.00020000', 'amount': '0.20513671', 'duration': 2, 'autoRenew': 0, 'date': '2019-01-06 08:42:47'}]}
# my_open_offers = []

if my_open_offers and 'BTC' in my_open_offers:
    for i in range(len(my_open_offers['BTC'])):

        now = datetime.datetime.now()
        date = my_open_offers['BTC'][i]['date']
        dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        print((now - dt).total_seconds() / 60 - 180)

        if ( (now - dt).total_seconds() / 60 - 180) > 30:
            try:
                #cancel = my_polo.cancelLoanOffer(orderNumber=my_open_offers['BTC'][i]['id'])
                #print(cancel)
                pass
            except:
                print("Error cancelling order ID:", my_open_offers['BTC'][i]['id'])
elif not my_open_offers:
    print("No open offers")
else:
    print("Error")