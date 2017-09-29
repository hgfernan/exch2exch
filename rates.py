# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 23:25:51 2017

@author: hilton
"""
import math           # trunc()
import time           # time()
import datetime       # class datetime
import urllib.request # urlopen()

class Rate: 
    def __init__ (self, source, target, rate): 
        self.source = source
        self.target = target
        self.rate   = rate        
        
class Rates:
#    def __init__ (self):
#        print (self.__class__.__name__)
    
    def getBrl2Usd (self):
        return self.brl2usd
    
    def getUsd2Brl (self):
        return self.usd2brl
    
    def getServiceName (self):
        return self.service
    
    def getServicePrefix (self):
        return self.prefix
        
    def __str__ (self):
        result = ''

        service = self.service
        dt      = self.dt
        usd2brl = self.usd2brl
        brl2usd = self.brl2usd
        ftupl = (service, dt, usd2brl, brl2usd)
        
        result = "{0}: {1}: USD2BRL {2:.4f}, BRL2USD {3:.4f}".format (*ftupl)

        return result        
    
    pass 

def google_get_rate (url):
    result = 0

    f = urllib.request.urlopen (url)
    
    try:
        line = f.readline ()
        while line != b'':
            ind = line.find (b'currency_converter')
            if ind != -1:
                
                fields = line.split ()
                rate = fields[5].split (b'>')[1]
                
                break
                
            line = f.readline ()
        
        result = float (rate)
    except IndexError as err:
        result = 0.0
        
        fmt = "Google.get_rate(): {0}"
        print (fmt.format (err))
        
        raise
    
    # Normal function termination
    return result

G_U_USD2BRL = 'https://finance.google.com/finance/converter?a=1&from=USD&to=BRL&meta=ei%3DoKi6WfnPAsSTeoKNoJAB'
G_U_BRL2USD = 'https://finance.google.com/finance/converter?a=1&from=BRL&to=USD&meta=ei%3DYqi6Wej-AoyEeoLbh9gF'
    
class Google (Rates):
    #    U_USD2BRL = 'https://www.google.com/finance/converter?a=1&from=USD&to=BRL'
    U_USD2BRL = 'https://finance.google.com/finance/converter?a=1&from=USD&to=BRL&meta=ei%3DoKi6WfnPAsSTeoKNoJAB'
#    U_BRL2USD = 'https://www.google.com/finance/converter?a=1&from=BRL&to=USD'
    U_BRL2USD = 'https://finance.google.com/finance/converter?a=1&from=BRL&to=USD&meta=ei%3DYqi6Wej-AoyEeoLbh9gF'

    def __init__ (self):
        ts = math.trunc (time.time () + 0.5)
        self.dt = datetime.datetime.fromtimestamp (ts)
                
        self.usd2brl = google_get_rate (Google.U_USD2BRL)
        self.brl2usd = google_get_rate (Google.U_BRL2USD)
                
        self.service = "Google"
        self.prefix = "ggl"
                
        # Normal function termination
        return
            
class XRates (Rates):
    U_XRATES = 'http://www.x-rates.com/table/?from=USD&amount=1'

    def get_rates ():        
        # Adding a fake browser User-Agent to make site x-rates.com happy
        headers = {'User-Agent' : 'Mozilla 5.10'}
            
        # Create the Request, joining URL and User-Agent
        request = urllib.request.Request (XRates.U_XRATES, headers = headers)
    
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
                    
            if line.find (b'from=USD') != -1:
                fields = line.split (b'>')
                
                susd = fields[2].split (b'<')[0]
                usd2brl = float (susd)
            
            elif line.find (b'from=BRL') != -1:
                fields = line.split (b'>')
                
                sbrl = fields[2].split (b'<')[0]
                brl2usd = float (sbrl)
                
        result = (usd2brl, brl2usd)
        
        return result

    def __init__ (self):
#        print (self.__class__.__name__)

        ts = math.trunc (time.time () + 0.5)
        self.dt = datetime.datetime.fromtimestamp (ts)

        self.usd2brl, self.usd2brl = XRates.get_rates () 
                
        self.service = "XRates"
        self.prefix = "xr"

# class Yahoo (Rates):
#    pass

