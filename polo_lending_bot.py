#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 23:18:58 2018

@author: romanromanenko
"""

from poloniex_api import Poloniex
from polo_config import *

my_polo = Poloniex(
  API_KEY = key,
  API_SECRET = secret)

balance = my_polo.returnAvailableAccountBalances("lending")
av_balance = float(balance['lending']['BTC'])

if av_balance >= 0.01:

    loan_offers = my_polo.returnLoanOrders(currency='BTC')
    amount = 0
    for i in range(len(loan_offers['offers'])):
        amount += float(loan_offers['offers'][i]['amount'])
        if amount > 2:
            break

    if i: i -= 1

    pos_info = my_polo.createLoanOffer(
            currency='BTC',
            amount=av_balance,
            duration=2,
            autoRenew=0,
            lendingRate=float(loan_offers['offers'][i]['rate'])
            )

    # send an email with all details
    server = smtplib.SMTP('smtp.gmail.com', 587)
    #server.ehlo()
    server.starttls()

    # Email details in config file
    server.login(from_email, from_email_pass)

    msg = "\r\n".join([
            "From: " + from_email,
            "To: " + to_email,
            "Subject: BTC loans at Polo today",
            "",
            str(pos_info)
        ])

    server.sendmail(from_email, to_email, msg)
    server.quit()
