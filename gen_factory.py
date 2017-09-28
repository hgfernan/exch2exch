# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:17:53 2017

@author: hilton
"""
import sys # exit()

class Dummy: 
    def __init__ (self):
        print ("{0}.__init__() ".format (self.__class__.__name__))

class Dummy1 (Dummy):
    def __init__ (self):
        print ("{0}.__init__() ".format (self.__class__.__name__))
        
#    def __new__ (self):
#        print ("Dummy1.__new__() ", self.__class__.__name__)
#        Dummy1.__init__ (self)
        
    def doSomething (self):
        print ("I'm an instance of class {0}". format (type (self).__name__))

class Dummy2 (Dummy):
    def doSomething (self):
        print ("I'm an instance of class {0}".format (type (self).__name__))

class Dummy3 (Dummy):
    def doSomething (self):
        print ("I'm an instance of class {0}".format (type (self).__name__))

class GenFactory:
    def __init__ (self, cls):
        types = cls.__subclasses__ ()
        
#        print (self.types)
        
        self.classes = {}
        for cls in types:
            self.classes[cls.__name__] = cls
            
    def validClassNames (self):
        return self.classes.keys ()
    
    def genObject (self, name):
        result = None 
        
        if name in self.classes:
                cls = self.classes[name]
                result = cls.__new__ (cls)
                
                result.__init__ ()
                
        return result
        
def main ():
    gf = GenFactory (Dummy)
    
#    obj = gf.genObject ("Dummy2")
#    
#    nam = type (obj).__name__ 
#    print ("type (obj).__name__ = {0}".format (nam))
#    
#    obj.doSomething ()
#    print ("="*12)
    
    for cn in gf.validClassNames ():
        print ("Class {0}".format (cn))
        obj = gf.genObject (cn)
    
        nam = type (obj).__name__ 
        print ("type (obj).__name__ = {0}".format (nam))
        obj.doSomething ()
        print ()
        
    # Normal function termination
    return 0

if __name__ == '__main__':
    sys.exit (main ())