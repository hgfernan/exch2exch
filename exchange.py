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
* https://docs.python.org/3.4/library/json.html
"""

import sys            # exit()
import json           # load()
import datetime       # class datetime
import urllib.request # urlopen()

# TODO refactor classes so they are lazy -- work only when necessary

# TODO A class ExchangeData can encapsulate the returns of exchanges

class DatetimeEncoder (json.JSONEncoder):
    def default(self, obj):
        if isinstance (obj, datetime.datetime):
            return obj.__repr__ ()
            
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

# Standard way of packing oderdebook information across all exchange classes
        
class OrderBook:
    pass

# Standard way of packing ticker information across all exchange classes
        
class Ticker:
    def __init__ (self):
        pass
    
    def __str__ (self):
        result = ''
        
        result = json.dumps (self.__dict__)       
        
        # Normal function termination
        return result

# Standard way of packing trades information across all exchange classes
        
        
class Trades:
    pass

class Exchange:
    U_TICKER = ''
    U_TRADES = ''
    U_ORDRBK = ''

# TODO implement
    
    def __init__ (self):
#        self.dnload_ticker ()
#        self.process_ticker ()
        pass
    
    def dnload_ticker (self):
        url = self.__class__.U_TICKER
#        print (url)
        f = urllib.request.urlopen (url)
        
        line = f.readline ()
#        print (line)
        
        self.ticker = json.loads (line.decode (encoding='utf-8'))
#        print (self.ticker)
        
    def process_ticker (self):
        # TODO raise exception
        pass
    
    def get_ticker (self):
        self.dnload_ticker ()
        self.process_ticker ()
    
    def dnload_trades (self):
        url = self.__class__.U_TRADES
#        print (url)
        f = urllib.request.urlopen (url)
        
        line = f.readline ()
#        print (line)
        
        self.trades = json.loads (line.decode (encoding='utf-8'))
#        print (self.ticker)
        
    def process_trades (self):
        # TODO raise exception
        pass
    
    def get_trades (self):
        self.dnload_trades ()
        self.process_trades ()
    
    def dnload_orderbook (self):
        url = self.__class__.U_ORDRBK
        f = urllib.request.urlopen (url)
        
        line = f.readline ()
#        print (line)
        
        self.trades = json.loads (line.decode (encoding='utf-8'))
#        print (self.ticker)
        
    def process_orderbook (self):
        # TODO raise exception
        pass
    
    def get_orderbook (self):
        self.dnload_orderbook ()
        self.process_orderbook ()
    
    
    def get_exch_name (self):
        # TODO raise exception
        pass
        
    def __str__ (self):
        # TODO raise exception
        pass
        
    def __repr__ (self):
        result = "{0} ()".format (type (self).__name__)
        
        # Normal function termination
        return result
        
class FoxBit (Exchange):
    U_TICKER = 'https://api.blinktrade.com/api/v1/BRL/ticker?crypto_currency=BTC'
    
    def __init__ (self):
        super ().__init__ ()
        
    def process_ticker (self):
        # TODO get the date from the computer ?
#        self.ts   = int   (self.ticker['date'])
        self.ticker['date'] = datetime.datetime.now ()
        # TODO generate ts from dt
     
    def get_ticker (self):
        super ().get_ticker ()
        
        buy  = float (self.ticker['buy'])
        sell = float (self.ticker['sell'])
        high = float (self.ticker['high'])
        low  = float (self.ticker['low'])
        dt   = self.ticker['date']
        
        result = (dt, sell, buy, high, low)
        
        return result
        
    def process_trades (self):
        # TODO get the date from the computer ?
#        self.ts   = int   (self.ticker['date'])
        self.buy  = float (self.ticker['buy'])
        self.sell = float (self.ticker['sell'])
        self.high = float (self.ticker['high'])
        self.low  = float (self.ticker['low'])
    
        self.dt = datetime.datetime.now ()
        # TODO generate ts from dt
     
    def get_trades (self):
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
        
    def __str__ (self):
        result = json.dumps (self.__dict__, cls = DatetimeEncoder)
        
        # Normal function termination
        return result
                
class MercadoBitcoin (Exchange):
    U_TICKER = 'https://www.mercadobitcoin.net/api/ticker/'
    U_ORDRBK = 'https://www.okcoin.com/api/v1/depth.do?symbol=btc_usd'
    U_TRADES = 'https://www.okcoin.com/api/v1/trades.do?symbol=btc_usd'
    
    def __init__ (self):
        super ().__init__ ()
        
    def process_ticker (self):
#        myClass = type (self).__name__
#        print ("{0}.process_ticker ()".format (myClass))
        self.ts   = int   (self.ticker['ticker']['date'])
        self.buy  = float (self.ticker['ticker']['buy'])
        self.sell = float (self.ticker['ticker']['sell'])
        self.high = float (self.ticker['ticker']['high'])
        self.low  = float (self.ticker['ticker']['low'])
    
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
        
    def __str__ (self):
        result = json.dumps (self.__dict__, cls = DatetimeEncoder)
        
        # Normal function termination
        return result
        
class OkCoin (Exchange):
    U_TICKER = 'https://www.okcoin.com/api/v1/ticker.do?symbol=btc_usd'
    
    def __init__ (self):
        super ().__init__ ()
        
    def process_ticker (self):
        self.ts   = int   (self.ticker['date'])
        self.buy  = float (self.ticker['ticker']['buy'])
        self.sell = float (self.ticker['ticker']['sell'])
        self.high = float (self.ticker['ticker']['high'])
        self.low  = float (self.ticker['ticker']['low'])
    
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
        
    def __str__ (self):
        result = json.dumps (self.__dict__, cls = DatetimeEncoder)
        
        # Normal function termination
        return result

def main ():
    exchanges = []
    exchanges.append (FoxBit ())
    exchanges.append (MercadoBitcoin ())
    exchanges.append (OkCoin ())
    
    for exch in exchanges:
        exch.get_ticker ()
        
        print ( "{0}:".format (exch.get_exch_name ()) )
        print ( "\t{0}".format (exch) )
    
    return 0
    
if __name__ == '__main__':
    sys.exit (main ())
