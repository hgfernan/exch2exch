#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 18:45:22 2017

@author: hilton
"""

# Standard way of packing ticker information across all exchange classes

import json 
import time       # class time

import start_time
        
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
        
        self.startDt = start_time.getTimeAsInt ()
        
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
    
    def getStartDt (self):
        return self.startDt

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
        
        fmt    = '{0}, coin pair {1}\n' 
        result = fmt.format (self.exch, self.pair)
        
        gm = time.gmtime (self.dt)
        result += '\ttimestamp: ' + time.strftime ('%Y-%m-%d %H:%M:%S', gm) 
        gm = time.gmtime (self.startDt)
        result += ", program started: " + \
            time.strftime ('%Y-%m-%d %H:%M:%S', gm) 
        result += "\n"
        
        fmt     = '\tbuy/sell: {0:.8f}/{1:.8f}, '
        result += fmt.format (self.buy, self.sell)
        
        fmt     = 'high/low: {0:.8f}/{1:.8f}, '
        result += fmt.format (self.high, self.low)
        
        fmt     = 'last: {0:.8f}, volume: {1:.8f}\n'
        result += fmt.format (self.last, self.vol)
        
        # Normal function termination
        return result
