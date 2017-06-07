#! /usr/bin/env python3 

# -*- coding: utf-8 -*-
"""
A testbed for URL parsing of the exch2exch project

Created on Tue Jun  6 23:23:43 2017

@author: hilton
From 
* https://docs.python.org/3.4/library/urllib.request.html#module-urllib.request
* http://www.pythonforbeginners.com/python-on-the-web/how-to-use-urllib2-in-python/]
* https://www.mercadobitcoin.com.br/api-doc/
"""

import math           # trunc()  
import time           # time()  
import json           # loads()  
import datetime       # class Datetime  
import urllib.request # class Request, urlopen()

# 
# 
# Google section 
#

def get_google_rate (url):
    result = 0

    f = urllib.request.urlopen (url)
    
    line = f.readline ()
    while line != b'':
        ind = line.find (b'currency_converter')
        if ind != -1:
            print (ind)
            print (line)
            
            fields = line.split ()
            print (fields[5])
            rate = fields[5].split (b'>')[1]
            print (rate)
            
            break
            
        line = f.readline ()
    
    result = float (rate)
    
    return result
    
def get_google_rates (urls):
    ts = math.trunc (time.time () + 0.5)
    dt = datetime.datetime.fromtimestamp (ts)
    
    # TODO round the seconds fraction
    
    usd2brl = urls[0]
    brl2usd = urls[1]
    
    usd = 0
    brl = 0
    
    usd = get_google_rate (usd2brl)
    brl = get_google_rate (brl2usd)
    
    result = (dt, usd, brl)
    
    return result
        
def get_x_rates (url):
    ts = math.trunc (time.time () + 0.5)
    dt = datetime.datetime.fromtimestamp (ts)
    
    # TODO round the seconds fraction
    
    # Adding a fake browser User-Agent to make site x-rates.com happy
    headers = {'User-Agent' : 'Mozilla 5.10'}
        
    # Create the Request, joining URL and User-Agent
    request = urllib.request.Request (url, headers = headers)

    # Open the URL as file
    f = urllib.request.urlopen (request)
    
    # Input over the file to get the rates
    line = None
    while line != b'':
        line = f.readline ()
        ind = line.find (b'BRL')
        if ind == -1:
            continue 
        
        ind = line.find (b'rtRates')
        if ind == -1:
            continue 
        
        print (line)
        
        if line.find (b'from=USD') != -1:
            print ('\nfields')
            fields = line.split (b'>')
            
            print (fields[2])
            susd = fields[2].split (b'<')[0]
            print (susd)
            usd = float (susd)
            print (usd)
            print ('\n')
        
        elif line.find (b'from=BRL') != -1:
            print ('\nfields')
            fields = line.split (b'>')
            
            print (fields[2])
            sbrl = fields[2].split (b'<')[0]
            print (sbrl)
            brl = float (sbrl)
            print (brl)
            print ('\n')
            
    result = (dt, usd, brl)
    
    return result

def get_mb_rates (url):
    f = urllib.request.urlopen (url)
    
    line = f.readline ()
    
    rv = json.loads (line.decode (encoding='utf-8'))
    
    ts   = rv['ticker']['date']
    buy  = rv['ticker']['buy']
    sell = rv['ticker']['sell']
    
    dt = datetime.datetime.fromtimestamp (float (ts))
    
    result = (dt, sell, buy)
    
    return result

def get_ok_rates (url):
    pass
    
usd2brl = 'https://www.google.com/finance/converter?a=1&from=USD&to=BRL'
# rv = get_google_rate (usd2brl)
# print (rv)

brl2usd = 'https://www.google.com/finance/converter?a=1&from=BRL&to=USD'
# rv = get_google_rate (brl2usd)
# print (rv)

urls = (usd2brl, brl2usd)

dt, usd, brl = get_google_rates (urls)

print ("Google: {0}: USD2BRL {1}, BRL2USD {2}".format (dt, usd, brl))
print ()

#
#
# X-rates section 
# 

url = 'http://www.x-rates.com/table/?from=USD&amount=1'
dt, usd, brl = get_x_rates (url)
print ("X-rates: {0}: USD2BRL {1}, BRL2USD {2}".format (dt, usd, brl))
print ()

#
#
# MercadoBitcoin section 
# 

url = 'https://www.mercadobitcoin.net/api/ticker/'

mb = get_mb_rates (url)
dt, sell, buy = mb    
print (mb)
print ("MercadoBitcoin: {0}: Sell {1} BRL, Buy {2} BRL".format (*mb))
print ()
 