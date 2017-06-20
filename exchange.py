# -*- coding: utf-8 -*-
"""
Classes to get data from selected Bitcoin exchanges.

Created on Sat Jun 17 13:01:13 2017

@author: hilton
From 
* https://docs.python.org/3.4/library/urllib.request.html#module-urllib.request
* http://www.pythonforbeginners.com/python-on-the-web/how-to-use-urllib2-in-python/
* https://www.mercadobitcoin.com.br/api-doc/
* https://blinktrade.com/docs/
"""

import sys            # exit()
import json           # load()
import datetime       # class datetime
import urllib.request # urlopen()

# TODO refactor classes so they are lazy -- work only when necessary

class Exchange:
    U_TICKER = ''
    U_TRADES = ''
    U_ORDRBK = ''

# TODO implement
    
    def __init__ (self):
#        self.process_url ()
#        self.process_json ()
        pass
    
    def process_url (self):
        url = self.__class__.U_TICKER
#        print (url)
        f = urllib.request.urlopen (url)
        
        line = f.readline ()
#        print (line)
        
        self.json = json.loads (line.decode (encoding='utf-8'))
#        print (self.json)
        
    def process_json (self):
        # TODO raise exception
        pass
    
    def get_ticker (self):
        self.process_url ()
        self.process_json ()
    
    def get_exch_name (self):
        # TODO raise exception
        pass
        
    def __str__ (self):
        result = str (self.json)
    
        return result
        
    def __repr__ (self):
        result = "{0} ()".format (type (self).__name__)
        
        # Normal function termination
        return result
        
class FoxBit (Exchange):
    U_TICKER = 'https://api.blinktrade.com/api/v1/BRL/ticker?crypto_currency=BTC'
    
    def __init__ (self):
        super ().__init__ ()
        
    def process_json (self):
        # TODO get the date from the computer ?
#        self.ts   = int   (self.json['date'])
        self.buy  = float (self.json['buy'])
        self.sell = float (self.json['sell'])
        self.high = float (self.json['high'])
        self.low  = float (self.json['low'])
    
        self.dt = datetime.datetime.now ()
        # TODO generate ts from dt
     
    def get_ticker (self):
        super ().get_ticker ()
        
        buy  = self.buy
        sell = self.sell
        high = self.high
        low  = self.low
        dt   = self.dt
        
        result = (dt, sell, buy, high, low)
        
        return result
    
    def get_exch_name (self):
        return "FoxBit"
                
class MercadoBitcoin (Exchange):
    U_TICKER = 'https://www.mercadobitcoin.net/api/ticker/'
    
    def __init__ (self):
        super ().__init__ ()
        
    def process_json (self):
#        myClass = type (self).__name__
#        print ("{0}.process_json ()".format (myClass))
        self.ts   = int   (self.json['ticker']['date'])
        self.buy  = float (self.json['ticker']['buy'])
        self.sell = float (self.json['ticker']['sell'])
        self.high = float (self.json['ticker']['high'])
        self.low  = float (self.json['ticker']['low'])
    
        self.dt = datetime.datetime.fromtimestamp (float (self.ts))
    
    def get_ticker (self):
        super ().get_ticker ()
        
        buy  = self.buy
        sell = self.sell
        high = self.high
        low  = self.low
        dt   = self.dt
        
        result = (dt, sell, buy, high, low)
        
        return result
    
    def get_exch_name (self):
        return "Mercado Bitcoin"
        
class OkCoin (Exchange):
    U_TICKER = 'https://www.okcoin.com/api/v1/ticker.do?symbol=btc_usd'
    
    def __init__ (self):
        super ().__init__ ()
        
    def process_json (self):
        self.ts   = int   (self.json['date'])
        self.buy  = float (self.json['ticker']['buy'])
        self.sell = float (self.json['ticker']['sell'])
        self.high = float (self.json['ticker']['high'])
        self.low  = float (self.json['ticker']['low'])
    
        self.dt = datetime.datetime.fromtimestamp (float (self.ts))
    
    def get_ticker (self):
        super ().get_ticker ()
        
        buy  = self.buy
        sell = self.sell
        high = self.high
        low  = self.low
        dt   = self.dt
        
        result = (dt, sell, buy, high, low)
        
        return result
    
    def get_exch_name (self):
        return "OkCoin"

def main ():
    exchanges = []
    exchanges.append (FoxBit ())
    exchanges.append (MercadoBitcoin ())
    exchanges.append (OkCoin ())
    
    for exch in exchanges:
        exch.get_ticker ()
        
        print ("{0}: {1}".format (exch.get_exch_name (), exch))
    
    return 0
    
if __name__ == '__main__':
    sys.exit (main ())
