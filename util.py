# -*- coding: utf-8 -*-
import web
import random
import settings

def accept_code():
    return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for x in range(6))

def sendmail(recip, accept_str):
    accept_url = settings.SITE_URL + '/accept/' + accept_str
    web.sendmail(settings.FROM, recip, settings.SUBJECT, settings.MESSAGE % accept_url)
