#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 23:18:58 2018

@author: romanromanenko
"""

from poloniex_api import Poloniex
from polo_config import *
import smtplib      #import for SMTP
import datetime     #import for comparing open loans time with now()

# send an email with all details
def email_send(subj, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.ehlo()
    server.starttls()

    # Email details in config file
    server.login(from_email, from_email_pass)

    msg = "\r\n".join([
        "From: " + from_email,
        "To: " + to_email,
        subj,
        "",
        message
    ])

    server.sendmail(from_email, to_email, msg)
    server.quit()

# api key/secret pair for lending in config file
my_polo = Poloniex( API_KEY = key_lend, API_SECRET = secret_lend)

def cancel_loans():
    # getting my open loan offers
    # e.g. my_open_offers = {'BTC': [{'id': 1053294329, 'rate': '0.00020000', 'amount': '0.20513671', 'duration': 2, 'autoRenew': 0, 'date': '2019-01-06 08:42:47'}]}
    my_open_offers = my_polo.returnOpenLoanOffers()

    # if server returns something and there are offers in the response ...
    if my_open_offers and 'BTC' in my_open_offers:

        # ... cycle through all offers and compare offer datetime with now
        # if offer was placed more than 30 min ago, cancel it
        for i in range(len(my_open_offers['BTC'])):

            now = datetime.datetime.now()
            date = my_open_offers['BTC'][i]['date']
            dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

            if ((now - dt).total_seconds() / 60 - 180) > 10:
                try:
                    cancel = my_polo.cancelLoanOffer(orderNumber=my_open_offers['BTC'][i]['id'])
                except:
                    email_send("Polo: error", "Error cancelling order ID:" + str(my_open_offers['BTC'][i]['id']))
    elif not my_open_offers:
        pass
    else:
        email_send("Polo: error", "Error response for my open offers")

#cancel loans that haven't been claimed for more than 30 min
cancel_loans()

# getting balance from poloniex, e.g. {'exchange': {'BTT': '500.00000000'}, 'lending': {'BTC': '0.00016670'}}
balance = my_polo.returnAvailableAccountBalances()

# if balance not empty and available balance is larger than minimal lending amount of 0.005 BTC
if 'lending' in balance and float(balance['lending']['BTC']) > 0.005:

    av_balance = float(balance['lending']['BTC'])
    loan_offers = my_polo.returnLoanOrders(currency='BTC')
    amount = 0
    for i in range(len(loan_offers['offers'])):
        amount += float(loan_offers['offers'][i]['amount'])
        if amount > 2:
            break

    if i: i -= 1

    pos_info = my_polo.createLoanOffer(
            currency='BTC',
            amount = av_balance,
            duration=2,
            autoRenew=0,
            lendingRate=float(loan_offers['offers'][i]['rate'])
            )

    if 'success' not in pos_info:
        pos_info['amount'] = av_balance
        pos_info['rate'] = ("%f" % float(loan_offers['offers'][i]['rate']) )
        email_send("Subject: BTC loans at Polo today", str(pos_info))

