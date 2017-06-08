#! /usr/bin/env python3 

# -*- coding: utf-8 -*-
"""
A tool to compare the prices of two Bitcoin exchanges.

Created on Thu Jun  8 08:18:45 2017

@author: hilton
From 
* https://docs.python.org/3.4/library/urllib.request.html#module-urllib.request
* http://www.pythonforbeginners.com/python-on-the-web/how-to-use-urllib2-in-python/
* https://www.mercadobitcoin.com.br/api-doc/
"""

import math           # trunc()  
import time           # time()  
import json           # loads()  
import datetime       # class Datetime  
import urllib.request # class Request, urlopen()

class Rates:
    def __init__ (self, dt, usd2brl, brl2usd, service):
        self.dt  = dt
        self.usd2brl = usd2brl
        self.brl2usd = brl2usd
        self.service = service
    
    def getBrl2Usd (self):
        return self.brl2usd
    
    def getUsd2Brl (self):
        return self.usd2brl
    
    def getServiceName (self):
        return self.service
        
    def __str__ (self):
        result = ''

        service = self.service
        dt      = self.dt
        usd2brl = self.usd2brl
        brl2usd = self.brl2usd
        ftupl = (service, dt, usd2brl, brl2usd)
        
        result = "{0}: {1}: USD2BRL {2:.4f}, BRL2USD {3:.4f}".format (*ftupl)

        return result        
        
class XbtPrices:
    def __init__ (self, dt, sell, buy, exch, coin):
        self.dt   = dt
        self.sell = sell
        self.buy  = buy
        self.exch = exch
        self.coin = coin
        
    def getDateTime (self):
        return self.dt
        
    def getBuy (self):
        return self.buy
        
    def getSell (self):
        return self.sell
        
    def getExchangeName (self):
        return self.exch
        
    def getCoinName (self):
        return self.coin

    def __str__ (self):
        result = ''
        
        dt, sell, buy = self.dt, self.sell, self.buy
        exch, coin   = self.exch, self.coin
        ftpl = exch, dt, sell, coin, buy
        result = "{0}: {1}: Sell {2:.4f} {3}, Buy {4:.4f} {3}".format (*ftpl)
        
        return result
        
class Differences:
    def __init__ (self, rates, mb, ok):
        self.rates = rates
        self.mb = mb
        self.ok = ok
        
        self.dmin = mb.getBuy () - ok.getBuy ()
        
        self.dmax = mb.getSell () - ok.getBuy ()
        
    def getMinDelta (self):
        return self.dmin
        
    def getMaxDelta (self):
        return self.dmax
        
    def __str__ (self):
        result = ""
        
        oname = self.ok.getExchangeName ()
        mname = self.ok.getExchangeName ()
        sname = self.rates.getServiceName ()
        
        fmt = "Calculation between {0} and {1} rates, with conversion from {1}"
        result = fmt.format (oname, mname, sname)
        fmt = "\nIntervals: minimum {0:.4f}, maximum {1:.4f}"
        result += fmt.format (self.getMinDelta (), self.getMaxDelta ())
        return result

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
#            print (ind)
#            print (line)
            
            fields = line.split ()
#            print (fields[5])
            rate = fields[5].split (b'>')[1]
#            print (rate)
            
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
        
#        print (line)
        
        if line.find (b'from=USD') != -1:
#            print ('\nfields')
            fields = line.split (b'>')
            
#            print (fields[2])
            susd = fields[2].split (b'<')[0]
#            print (susd)
            usd = float (susd)
#            print (usd)
#            print ('\n')
        
        elif line.find (b'from=BRL') != -1:
#            print ('\nfields')
            fields = line.split (b'>')
            
#            print (fields[2])
            sbrl = fields[2].split (b'<')[0]
#            print (sbrl)
            brl = float (sbrl)
#            print (brl)
#            print ('\n')
            
    result = (dt, usd, brl)
    
    return result

def get_mb_rates (url):
    f = urllib.request.urlopen (url)
    
    line = f.readline ()
    
    rv = json.loads (line.decode (encoding='utf-8'))
    
    ts   = int   (rv['ticker']['date'])
    buy  = float (rv['ticker']['buy'])
    sell = float (rv['ticker']['sell'])
    
    dt = datetime.datetime.fromtimestamp (float (ts))
    
    result = (dt, sell, buy)
    
    return result

def get_ok_rates (url):
    f = urllib.request.urlopen (url)
    
    line = f.readline ()
    
    rv = json.loads (line.decode (encoding='utf-8'))
    
    ts   = int   (rv['date'])
    buy  = float (rv['ticker']['buy'])
    sell = float (rv['ticker']['sell'])
    
    dt = datetime.datetime.fromtimestamp (float (ts))
    
    result = (dt, sell, buy)
    
    return result
    
u_usd2brl = 'https://www.google.com/finance/converter?a=1&from=USD&to=BRL'

u_brl2usd = 'https://www.google.com/finance/converter?a=1&from=BRL&to=USD'

urls = (u_usd2brl, u_brl2usd)

dt, usd2brl, brl2usd = get_google_rates (urls)

google = Rates (dt, usd2brl, brl2usd, "Google")

print (google)
print ()

#
#
# X-rates section 
# 

url = 'http://www.x-rates.com/table/?from=USD&amount=1'
dt, brl2usd, usd2brl = get_x_rates (url)

x_rates = Rates (dt, brl2usd, usd2brl, "X-Rates")

print (x_rates)
print ()

# TODO calculate avg USD2BRL rate

#
#
# MercadoBitcoin section 
# 

u_mb = 'https://www.mercadobitcoin.net/api/ticker/'

mb_tupl = get_mb_rates (u_mb)
dt, sell, buy = mb_tupl

mb = XbtPrices (dt, sell, buy, "MercadoBitcoin", "BRL")

# print ("MercadoBitcoin: {0}: Sell {1} BRL, Buy {2} BRL".format (mb))
print (mb)
 
brl2usd = google.getUsd2Brl ()

sell /= brl2usd
buy  /= brl2usd 
mb_usd = XbtPrices (dt, sell, buy, "MercadoBitcoin", "USD")
print (mb_usd)
print ()

#
#
# OkCoin section 
# 


u_ok = 'https://www.okcoin.com/api/v1/ticker.do?symbol=btc_usd'

ok_tupl = get_ok_rates (u_ok)
dt, sell, buy = ok_tupl

ok = XbtPrices (dt, sell, buy, "OkCoin", "USD")

# print ("MercadoBitcoin: {0}: Sell {1} BRL, Buy {2} BRL".format (mb))
print (ok)
print ()
 

diff = Differences (google, mb_usd, ok)

print (diff)