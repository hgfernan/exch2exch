#! /usr/bin/env python3 
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
import time           # time(), gmtime()
import json           # load(), dumps()
import datetime       # class datetime
import urllib.request # urlopen()

import start_time
import ticker

# TODO refactor classes so they are lazy -- work only when necessary

# TODO A class ExchangeData can encapsulate the returns of exchanges

class DatetimeEncoder (json.JSONEncoder):
    def default(self, obj):
        if isinstance (obj, datetime.datetime):
            return obj.__repr__ ()
            
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

        
class Exchange:
    U_TICKER = ''
    U_TRADES = ''
    U_ORDRBK = ''

# TODO implement orderbook and trades
    
    def __init__ (self):
#        self.dnload_ticker ()
#        self.process_ticker ()
        self.startDt = start_time.getTimeAsInt ()
    
    def dnload_ticker (self):
        url = self.__class__.U_TICKER
#        print (url)
        f = urllib.request.urlopen (url)
        
        line = f.readline ()
#        print (line)
        self.originalTicker = line.decode (encoding = 'utf-8')
        
        self.ticker = json.loads (line.decode (encoding='utf-8'))
#        print (self.ticker)
        
    def process_ticker (self):
        # TODO raise exception
        pass
    
    def get_ticker (self):
        self.dnload_ticker ()
        self.process_ticker ()
    
    def mkTicker (self): 
        # TODO raise exception
        pass
    
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
    
    def getOriginalTicker (self):
        # TODO raise exception
        pass
    
    def getCoinPair (self):
        # TODO raise exception
        pass
        
    def __str__ (self):
        # TODO raise exception
        pass
        
    def __repr__ (self):
        result = "{0} ()".format (type (self).__name__)
        
        # Normal function termination
        return result

class Bitfinex (Exchange):
    U_TICKER = 'https://api.bitfinex.com/v1/pubticker/btcusd'
    U_ORDRBK = 'https://api.bitfinex.com/v1/book/btcusd'
    U_TRADES = 'https://api.bitfinex.com/v1/trades/btcusd'
    
    def __init__ (self):
        super ().__init__ ()
 
    def process_ticker (self):
#        myClass = type (self).__name__
#        print ("{0}.process_ticker ()".format (myClass))
        self.exch = self.get_exch_name ()
        self.pair = 'BTCUSD'
        
        aux       = float (self.ticker['timestamp'])
        self.ts   = int   (aux)
        
        self.buy  = float (self.ticker['bid'])
        self.sell = float (self.ticker['ask'])
        self.high = float (self.ticker['high'])
        self.low  = float (self.ticker['low'])
        self.last = float (self.ticker['last_price'])
        self.vol  = float (self.ticker['volume'])
    
        self.dt = datetime.datetime.fromtimestamp (float (self.ts))
    
    def get_ticker (self):
        super ().get_ticker ()
        
        dt   = self.dt
        buy  = self.buy
        sell = self.sell
        high = self.high
        low  = self.low
        last = self.last
        
        result = (dt, sell, buy, high, low, last)
        
        return result
    
    def mkTicker (self):
        super ().get_ticker ()
        
        exch = self.exch
        pair = self.pair
        dt   = self.ts
        buy  = self.buy
        sell = self.sell
        high = self.high
        low  = self.low
        last = self.last
        vol  = self.vol
        
        result = \
            ticker.Ticker (exch, pair, dt, buy, sell, high, low, last, vol)
        
        return result
    
    def get_exch_name (self):
        return "Bitfinex"
    
    def get_exch_prefix (self):
        return "bf"
        
    def getOriginalTicker (self):
        return self.originalTicker
        
    def getCoinPair (self):
        return self.pair
        
    def __str__ (self):
        result = json.dumps (self.__dict__, cls = DatetimeEncoder)
        
        # Normal function termination
        return result      
        
class Bitstamp (Exchange):
    U_TICKER = 'https://www.bitstamp.net/api/ticker/'
    U_ORDRBK = 'https://www.bitstamp.net/api/order_book/'
    U_TRADES = 'https://www.bitstamp.net/api/transactions/'
      
    def __init__ (self):
        super ().__init__ ()
 
    def process_ticker (self):
#        myClass = type (self).__name__
#        print ("{0}.process_ticker ()".format (myClass))
        self.exch = self.get_exch_name ()
        self.pair = 'BTCUSD'
        self.ts   = int   (self.ticker['timestamp'])
        self.buy  = float (self.ticker['bid'])
        self.sell = float (self.ticker['ask'])
        self.high = float (self.ticker['high'])
        self.low  = float (self.ticker['low'])
        self.last = float (self.ticker['last'])
        self.vol  = float (self.ticker['volume'])
    
        self.dt = datetime.datetime.fromtimestamp (float (self.ts))
    
    def get_ticker (self):
        super ().get_ticker ()
        
        dt   = self.dt
        buy  = self.buy
        sell = self.sell
        high = self.high
        low  = self.low
        last = self.last
        
        result = (dt, sell, buy, high, low, last)
        
        return result
    
    def mkTicker (self):
        super ().get_ticker ()
        
        exch = self.exch
        pair = self.pair
        dt   = self.ts
        buy  = self.buy
        sell = self.sell
        high = self.high
        low  = self.low
        last = self.last
        vol  = self.vol
        
        result = \
            ticker.Ticker (exch, pair, dt, buy, sell, high, low, last, vol)
        
        return result
    
    def get_exch_name (self):
        return "Bitstamp"
    
    def get_exch_prefix (self):
        return "bs"
        
    def getOriginalTicker (self):
        return self.originalTicker
        
    def __str__ (self):
        result = json.dumps (self.__dict__, cls = DatetimeEncoder)
        
        # Normal function termination
        return result       
        
class FoxBit (Exchange):
    U_TICKER = 'https://api.blinktrade.com/api/v1/BRL/ticker?crypto_currency=BTC'
    
    def __init__ (self):
        super ().__init__ ()
        
    def process_ticker (self):
        tt = time.time ()
        self.ticker['ts'] = tt
        self.ticker['date'] = datetime.datetime.fromtimestamp (tt)
        self.exch = self.get_exch_name ()
        self.pair = "BTCBRL"
     
    def get_ticker (self):
        super ().get_ticker ()
        
        self.dt   = self.ticker['date']
        self.buy  = float (self.ticker['buy'])
        self.sell = float (self.ticker['sell'])
        self.high = float (self.ticker['high'])
        self.low  = float (self.ticker['low'])
        self.last = float (self.ticker['last'])
        
        result = (self.dt, self.sell, self.buy, self.high, self.low, self.last)
        
        return result
    
    def mkTicker (self): 
        super ().get_ticker ()
        
        exch = self.exch
        pair = self.pair
        ts   = self.ticker['ts']
        buy  = float (self.ticker['buy'])
        sell = float (self.ticker['sell'])
        high = float (self.ticker['high'])
        low  = float (self.ticker['low'])
        last = float (self.ticker['last'])
        vol  = float (self.ticker['last'])
        
        result = \
            ticker.Ticker (exch, pair, ts, buy, sell, high, low, last, vol)
        
        return result
        
    def process_trades (self):
        pass
     
    def get_trades (self):
        pass
    
    def get_exch_name (self):
        return "FoxBit"
        
    def __str__ (self):
        result = '{'
        
        result += 'buy : ' + str (self.buy) + ', '
        result += 'sell : ' + str (self.sell) + ', '
        result += 'high : ' + str(self.high) + ', '
        result += 'low  : ' + str (self.low) + ', '
        result += 'dt :  ' + str (self.dt)
        result += '}'
        # Normal function termination
        return result 
    
    def get_exch_prefix (self):
        return "fb"
        
    def getOriginalTicker (self):
        return self.originalTicker
                
class MercadoBitcoin (Exchange):
    U_TICKER = 'https://www.mercadobitcoin.net/api/ticker/'
    U_ORDRBK = 'https://www.mercadobitcoin.net/api/BTC/orderbook/'
    U_TRADES = 'https://www.mercadobitcoin.net/api/BTC/trades/'
    
    def __init__ (self):
        super ().__init__ ()
        
    def process_ticker (self):
#        myClass = type (self).__name__
#        print ("{0}.process_ticker ()".format (myClass))
        self.exch = self.get_exch_name ()
        self.pair = 'BTCBRL'
        self.ts   = int   (self.ticker['ticker']['date'])
        self.buy  = float (self.ticker['ticker']['buy'])
        self.sell = float (self.ticker['ticker']['sell'])
        self.high = float (self.ticker['ticker']['high'])
        self.low  = float (self.ticker['ticker']['low'])
        self.last = float (self.ticker['ticker']['last'])
        self.vol  = float (self.ticker['ticker']['vol'])
    
        self.dt = datetime.datetime.fromtimestamp (float (self.ts))
    
    def get_ticker (self):
        super ().get_ticker ()
        
        dt   = self.dt
        buy  = self.buy
        sell = self.sell
        high = self.high
        low  = self.low
        last = self.last
        
        result = (dt, sell, buy, high, low, last)
        
        return result
    
    def mkTicker (self):
        super ().get_ticker ()
        
        exch = self.exch
        pair = self.pair
        dt   = self.ts
        buy  = self.buy
        sell = self.sell
        high = self.high
        low  = self.low
        last = self.last
        vol  = self.vol
        
        result = \
            ticker.Ticker (exch, pair, dt, buy, sell, high, low, last, vol)
        
        return result
    
    def get_exch_name (self):
        return "MercadoBitcoin"
    
    def get_exch_prefix (self):
        return "mb"
        
    def getOriginalTicker (self):
        return self.originalTicker
        
    def __str__ (self):
        result = json.dumps (self.__dict__, cls = DatetimeEncoder)
        
        # Normal function termination
        return result
        
class OkCoin (Exchange):
    U_TICKER = 'https://www.okcoin.com/api/v1/ticker.do?symbol=btc_usd'
    
    def __init__ (self):
        super ().__init__ ()
        
    def process_ticker (self):
        self.exch = self.get_exch_name ()
        self.pair = 'BTCUSD'
        self.ts   = int   (self.ticker['date'])
        self.buy  = float (self.ticker['ticker']['buy'])
        self.sell = float (self.ticker['ticker']['sell'])
        self.high = float (self.ticker['ticker']['high'])
        self.low  = float (self.ticker['ticker']['low'])
        self.last = float (self.ticker['ticker']['last'])
        self.vol  = float (self.ticker['ticker']['vol'])
    
        self.dt = datetime.datetime.fromtimestamp (float (self.ts))
    
    def get_ticker (self):
        super ().get_ticker ()
        
        dt   = self.dt
        buy  = self.buy
        sell = self.sell
        high = self.high
        low  = self.low
        last = self.last
        
        result = (dt, sell, buy, high, low, last)
        
        return result
    
    def mkTicker (self):
        super ().get_ticker ()
        
        exch = self.exch
        pair = self.pair
        dt   = self.ts
        buy  = self.buy
        sell = self.sell
        high = self.high
        low  = self.low
        last = self.last
        vol  = self.vol
        
        result = \
            ticker.Ticker (exch, pair, dt, buy, sell, high, low, last, vol)
        
        return result
        
    def getOriginalTicker (self):
        return self.originalTicker
    
    def get_exch_name (self):
        return "OkCoin"
    
    def get_exch_prefix (self):
        return "okc"
        
    def __str__ (self):
        result = json.dumps (self.__dict__, cls = DatetimeEncoder)
        
        # Normal function termination
        return result

def main ():
    exchanges = []
    exchanges.append (Bitfinex ())
    exchanges.append (Bitstamp ())
    exchanges.append (FoxBit ())
    exchanges.append (MercadoBitcoin ())
    exchanges.append (OkCoin ())
    
    for exch in exchanges:
        exch.get_ticker ()
        
        print ( "{0}:".format (exch.get_exch_name ()) )
        print ( "\t{0}".format (exch) )
        
        ticker = exch.mkTicker ()
        print ( "\t{0}".format (ticker) )
        print ( "\tJSON: {0}".format (ticker.dumps ()) )
        
        print ( 'Original:\n\t{0}\n'.format (exch.getOriginalTicker ()) )
    
    return 0
    
if __name__ == '__main__':
    sys.exit (main ())
