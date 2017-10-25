#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 12:52:06 2017

@author: hilton
"""
import datetime # datetime

class Singleton (type):
    _instances = {}
    def __call__(self, *args, **kwargs):
        cls = self.__class__
        if cls not in cls._instances:
            cls._instances[cls] = \
                super (Singleton, cls).__call__ (self, *args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
                    
        return cls._instances[cls]
    
class DateTime (metaclass = Singleton):
    def __init__ (self):
        self.dt = datetime.datetime.now ()
        
        self.time = int (self.dt.timestamp () + 0.5)
    
    def getTimeAsInt (self):
        return self.time
    
    def getDatetime (self):
        return self.dt
    
    def __str__ (self):
        return self.dt.ctime ()

def __init__ ():
    _dt = DateTime ()
    
    fmt = '{0}.__init__() was called at {1}'
    print ( fmt.format (__package__, str (_dt)) )  
    
    _dt == _dt
    
def getTimeAsInt ():
    _dt = DateTime ()
    return _dt.getTimeAsInt ()

def getDatetime ():
    _dt = DateTime ()
    return _dt.getDatetime ()

if __name__ == __package__:
    __init__ ()
