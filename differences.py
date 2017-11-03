#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 19:03:02 2017

@author: hilton
"""

import json

import start_time

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
        
class DiffTicker (Differences):
    def __init__ (self, rates, destination, origin):
        super ().__init__ (rates, destination, origin)
        
        self.converted = False 
        self.brl2usd = 0.0
        self.convDstTicker = None
        
        self.aMax = 0
        self.aMin = 0
        
        self.rMin = 0
        self.rMax = 0
        
        self.aBuySell  = 0
        self.rBuySell = 0
        
        self.aLast = 0
        self.rLast = 0
        
        self.startDt = start_time.getTimeAsInt ()
        
    def calc (self):        
        org = self.orgTicker
        dst = self.dstTicker 
        
        # Check if the two tracks use the same pair
        if dst.getCoinPair () != org.getCoinPair ():
            # TODO create a more generic way to convert currencies
            self.brl2usd = self.rates.getBrl2Usd ()
            self.converted = True 
            
            pair = "USDBTC"
            
            self.convDstTicker = dst.convert (self.brl2usd, pair)
            dst = self.convDstTicker
    
        self.aMax = dst.getHigh () - org.getLow ()
        self.aMin = dst.getLow () - org.getHigh ()
        
        self.rMin = 100.0 * self.aMin / org.getHigh ()
        self.rMax = 100.0 * self.aMax / org.getLow ()
        
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
        
        result = ""
        
        # If destination coin was converted
        if self.converted:
            result += "Converted destination ticker\n"
            result += str (self.convDstTicker) + '\n'
        
        fmt     = "Calculation between {0} and {1} rates, "
        fmt    += "with conversion from {2}\n"
        result += fmt.format (origin, destination, rates)
        
        result += "Extrema\n"
        
        fmt = "\tAbsolute: Minimum {0:.4f}, Maximum {1:.4f}\n"
        result += fmt.format (self.aMin, self.aMax)
        
        fmt = "\tRelative: Minimum {0:.4f} %, Maximum {1:.4f} %\n"
        result += fmt.format (self.rMin, self.rMax)
        
        fmt = "\nBuy {0}, sell {1}\n"
        result += fmt.format (origin, destination)
        
        fmt = "\tAbsolute: {0:.4f}\n"
        result += fmt.format (self.aBuySell)
        
        fmt = "\tRelative: {0:.4f} %\n"
        result += fmt.format (self.rBuySell)
        
        fmt = "\nLast transactions at {0} and {1}\n"
        result += fmt.format (origin, destination)
        
        fmt = "\tAbsolute: {0:.4f}\n"
        result += fmt.format (self.aLast)
        
        fmt = "\tRelative: {0:.4f} %\n"
        result += fmt.format (self.rLast)
                
        # Normal function termination
        return result
    
    def dumps (self):
        # TODO create a report 
    
        fields = {}
        fields["startDt"]     = self.startDt
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

