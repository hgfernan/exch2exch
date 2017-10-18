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
    ## Constructor
    # @param exch Name of the exchange, a string not the object 
    # @param pair Pair of coins -- 1st target coin, 2nd source coin 
    # @param dt Date and time as seconds since 1970/01/01 at zero hours
    # @param buy Bid price
    # @param sell Ask price
    # @param high Highest price traded
    # @param low Lowest price traded
    # @param last Price of last trade
    # @param vol Volume traded
    def __init__ (self, exch, pair, dt, buy, sell, high, low, last, vol):
        self.exch = exch
        self.pair = pair
        self.dt   = dt
        self.buy  = buy 
        self.sell = sell 
        self.high = high 
        self.low  = low 
        self.last = last 
        self.vol  = vol 
        
    def convert (self, rate, destination):
        # TODO create a truly generic way of convert currencies
    
        exch = self.exch
        dt   = self.dt   * rate
        buy  = self.buy  * rate
        sell = self.sell * rate
        high = self.high * rate
        low  = self.low  * rate
        last = self.last * rate
        vol  = self.vol  * rate

        # TODO compare source and target
        pair = destination
        
        # TODO otherwise throw exception 
        
        result = Ticker (exch, pair, dt, buy, sell, high, low, last, vol)
        
        # Normal function termination
        return result 
        
    def getExchName (self):
        return self.exch
        
    def getCoinPair (self):
        return self.pair
        
    def getDt (self):
        return self.dt
    
    def getBuy (self):
        return self.buy
    
    def getSell (self):
        return self.sell
    
    def getHigh (self):
        return self.high
    
    def getLow (self):
        return self.low
    
    def getLast (self):
        return self.last
    
    def getVolume (self):
        return self.vol

    def mk_tuple (self): 
        result = (self.exch, self.pair, self.dt, self.buy, self.sell, \
            self.high, self.low, self.last, self.vol)
            
        # Normal function termination 
        return result
        
    def dumps (self):
        result = ''
        
        result = json.dumps (self.__dict__)       
        
        # Normal function termination
        return result
    
    def __str__ (self):
        result = ''
        
        fmt    = 'Exchange: {0}, coin pair {1}, ' 
        result = fmt.format (self.exch, self.pair)
        
        gm = time.gmtime (self.dt)
        result += 'timestamp: ' + time.strftime ('%Y-%m-%d %H:%M:%S', gm) 
        result += ", "
        
        fmt     = 'buy/sell: {0:.8f}/{1:.8f}, '
        result += fmt.format (self.buy, self.sell)
        
        fmt     = 'high/low: {0:.8f}/{1:.8f}, '
        result += fmt.format (self.high, self.low)
        
        fmt     = 'last: {0:.8f}, volume: {1:.8f}'
        result += fmt.format (self.last, self.vol)
        
        # Normal function termination
        return result

# Standard way of packing trades information across all exchange classes
        
        
class Trades:
    pass

class Exchange:
    U_TICKER = ''
    U_TRADES = ''
    U_ORDRBK = ''

# TODO implement orderbook and trades
    
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
        
class Differences:
    def __init__ (self, rates, destination, origin):
        self.rates     = rates
        self.dstTicker = destination
        self.orgTicker = origin
        self.coinPair  = self.orgTicker.getCoinPair ()
        
    def calc (self):
        pass
    
    def __str__ (self):
        result = "" 
        
        # Normal function termination
        return result
    
    def dumps (self):
        result = "" 
        
        # Normal function termination
        return result
        
class DiffOrderbook (Differences):
    pass
        
class DiffTracker (Differences):
    def __init__ (self, rates, destination, origin):
        super ().__init__ (rates, destination, origin)
        
        self.dmax = 0
        self.dmin = 0
        
        self.gmin = 0
        self.gmax = 0
        
        self.aBuySell  = 0
        self.rBuySell = 0
        
        self.aLast = 0
        self.rLast = 0
        
        
    def calc (self):        
        org = self.orgTicker
        dst = self.dstTicker 
        
        # Check if the two tracks use the same pair
        if dst.getCoinPair () != org.getCoinPair ():
            # TODO create a more generic way to convert currencies
            brl2usd = self.rates.getBrl2Usd ()
            pair = "USDBTC"
            dst = dst.convert (brl2usd, pair)
            
        self.aMax = dst.getHigh () - org.getLow ()
        self.aMin = dst.getLow () - org.getHigh ()
        
        self.rMin = 100.0 * self.dmin / org.getHigh ()
        self.rMax = 100.0 * self.dmax / org.getLow ()
        
        self.aBuySell  = dst.getBuy () - org.getSell ()
        self.rBuySell = 100.0 * self.aBuySell / org.getBuy ()
        
        self.aLast = dst.getLast () - org.getLast ()
        self.rLast = 100.0 * self.aLast / org.getLast ()
   
    def __str__ (self):
        # TODO create a report 
    
        # Calculation between Bitstamp and MercadoBitcoin rates, 
        # with conversion from Google + XRate
        origin      = self.orgTicker.getExchName ()
        destination = self.dstTicker.getExchName ()
        rates       = self.rates.getServiceName ()
        
        fmt     = "Calculation between {0} and {1} rates, "
        fmt    += "with conversion from {2}\n"
        result  = fmt.format (origin, destination, rates)
        
        result += "Extrema\n"
        
        fmt = "\tAbsolute: Minimum {0:.4f}, Maximum {1:.4f}\n"
        result += fmt.format (self.aMin, self.aMax)
        
        fmt = "\tRelative: Minimum {0:.4f}, Maximum {1:.4f}\n"
        result += fmt.format (self.rMin, self.rMax)
        
        fmt = "\nBuy {0}, sell {1}\n"
        result += fmt.format (origin, destination)
        
        fmt = "\tAbsolute: {0:.4f}\n"
        result += fmt.format (self.aBuySell)
        
        fmt = "\tRelative: {0:.4f}\n"
        result += fmt.format (self.rBuySell)
        
        fmt = "\nLast transactions at {0} and {1}\n"
        result += fmt.format (origin, destination)
        
        fmt = "\tAbsolute: {0:.4f}\n"
        result += fmt.format (self.aLast)
        
        fmt = "\tRelative: {0:.4f}\n"
        result += fmt.format (self.rLast)
                
        # Normal function termination
        return result
    
    def dumps (self):
        # TODO create a report 
    
        fields = {}
        fields["origin"]      = self.orgTicker.getExchName ()
        fields["destination"] = self.dstTicker.getExchName ()
        fields["rates"]       = self.rates.getServiceName ()
        
        fields["AbsMax"] = self.aMax
        fields["RelMax"] = self.rMax
        fields["AbsMin"] = self.aMin
        fields["RelMin"] = self.rMin
        
        fields["AbsBuySell"] = self.aBuySell
        fields["RelBuySell"] = self.rBuySell
        
        fields["AbsLast"] = self.aLast
        fields["RelLast"] = self.rLast
       
        result = json.dumps (fields)
         
        # Normal function termination
        return result
        
class DiffTrades (Differences):
    pass

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
        
        result = Ticker (exch, pair, dt, buy, sell, high, low, last, vol)
        
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
        
        result = Ticker (exch, pair, dt, buy, sell, high, low, last, vol)
        
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
        
        result = Ticker (exch, pair, ts, buy, sell, high, low, last, vol)
        
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
        
        result = Ticker (exch, pair, dt, buy, sell, high, low, last, vol)
        
        return result
    
    def get_exch_name (self):
        return "Mercado Bitcoin"
    
    def get_exch_prefix (self):
        return "mbt"
        
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
        
        result = Ticker (exch, pair, dt, buy, sell, high, low, last, vol)
        
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
