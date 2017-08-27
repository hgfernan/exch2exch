# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 12:30:41 2017

@author: hilton
From:
* Argparse Tutorial
  https://docs.python.org/3.5/howto/argparse.html
"""

import sys      # argv, exit()
import rates    # Google, XRates
import argparse # ArgumentParser, 
import datetime # datetime

import gen_factory # GenFactory
import exchange    # Exchange

class Args: 
    pass

class Application:
    def __init__ (self):
        d = datetime.datetime.now ()
        self.suffix = d.strftime ('%Y%m%d_%H%M')
        self.prefix = 'e2e'
    
    def parseCmdLine (self):
        desc = 'Compare two exchanges for a round operation'
        parser = argparse.ArgumentParser (description = desc)
        
        desc = 'Summary report (Default is stdout)' 
        parser.add_argument ('--summary', '-s', required = False,
                             help = desc)
        desc = 'File name for the conclusion of the arbitrage'
        parser.add_argument ('--conclusion', '-c', required = True,
                             help = desc)
        parser.add_argument ('--rates', '-r', default = 'Google',
                             help = 'Main rate service')
        parser.add_argument ('--origin', '-o', required = True,
                             help = 'Origin exchange')
        parser.add_argument ('--destination', '-d', required = True,
                             help = 'Destination exchange')
        parser.add_argument ('--verbose', '-v', action = "store_true",
                             help = 'Increase output verbosity')
                             
        args = parser.parse_args ()
        
        # TODO complete the copy of cmdline parameters
        
        result = Args ()
        result.summary     = args.summary 
        result.conclusion  = args.conclusion 
        result.rates       = args.rates 
        result.origin      = args.origin 
        result.destination = args.destination 
        result.verbose     = args.verbose
        
        self.args = result
        
        # Normal function termination
        return result
        
    def interpretArgs (self):
        # Open summary file
        if self.summary == None:
            try:
                sum_nam =  self.prefix + '_' + self.suffix + '.sum'
                self.sum_f = open (sum_nam, 'w')
                
            except IOError:
                # TODO an application specific msg here
                raise
        else:
            self.sum_f = sys.__stdout__
            
        # TODO Open output files for destination exchange
        try:
            cnc_nam  =  self.prefix + '_conclusion'
            cnc_nam += '_' + self.suffix + '.json'
            self.cnc_nam_f = open (cnc_nam, 'w')
            
        except IOError:
            # TODO an application specific msg here
            raise
            
        # TODO confirm that destinatian and origin exchanges are not equal
        args = self.args 
        if args.origin == args.destination:
            fmt = 'ERROR: Origin exchange {0} equal to destination {1}'
            msg = fmt.format (args.origin, args.destination)
            raise Exception (msg)

        # TODO get exchange names 
        gfExchange = gen_factory.GenFactory (exchange.Exchange)
        exch_names = gfExchange.validClassNames ()
            
        # TODO validate destination exchange
        if args.destination not in exch_names:
            fmt  = 'ERROR: Destination exchange {0} is not a valid '
            fmt += 'exchange name.\n'
            fmt += '\tShould be one of {1}'
            msg = fmt.format (args.destination, exch_names)
            raise Exception (msg)
            
        # TODO validate origin exchange
        if args.origin not in exch_names:
            fmt  = 'ERROR: Origin exchange {0} is not a valid exchange name.\n'
            fmt += '\tShould be one of {1}'
            msg = fmt.format (args.origin, exch_names)
            raise Exception (msg)
        
        # TODO open connection with destination exchange
        dstExchange = gfExchange.genObject (args.destination)
            
        # TODO Open output files for destination exchange
        try:
            dst_nam  =  self.prefix + '_' + dstExchange.get_exch_prefix ()
            dst_nam += '_' + self.suffix + '.json'
            self.e2e_dst_f = open (dst_nam, 'w')
            
        except IOError:
            # TODO an application specific msg here
            raise
            
        try:
            dst_nam  = dstExchange.get_exch_prefix ()
            dst_nam += '_' + self.suffix + '.json'
            self.dst_f = open (dst_nam, 'w')
            
        except IOError:
            # TODO an application specific msg here
            raise
            
        # TODO open connection with origin exchange
        orgExchange = gfExchange.genObject (args.origin)
            
        # TODO Open output files for origin exchange
        try:
            org_nam  =  self.prefix + '_' + orgExchange.get_exch_prefix ()
            org_nam += '_' + self.suffix + '.json'
            self.e2e_org_f = open (org_nam, 'w')
            
        except IOError:
            # TODO an application specific2 msg here
            raise
            
        try:
            org_nam  = orgExchange.get_exch_prefix ()
            org_nam += '_' + self.suffix + '.json'
            self.org_f = open (org_nam, 'w')
            
        except IOError:
            # TODO an application specific msg here
            raise
            
        # TODO open connection with main rate service
        gfRates = gen_factory.GenFactory (rates.Rates)
        rates_names = gfRates.validClassNames ()

        # TODO validate main rate service
        if args.rate not in rates_names:
            fmt  = 'ERROR: Main rates service {0} is not a valid rates name.\n'
            fmt += '\tShould be one of {1}'
            msg = fmt.format (args.rate, rates_names)
            raise Exception (msg)

        mainRate = gfRates.genObject (args.rate)
        
        # TODO Open output file for main rate service
        try:
            rat_nam  =  mainRate.getServicePrefix () + '_'
            rat_nam +=  self.suffix + '.rat'
            self.rat_f = open (rat_nam, 'w')
            
        except IOError:
            # TODO an application specific msg here
            raise        
            
        # TODO open connections with auxiliary rate services
        altRatesNames = []        
        for rateName in rates_names:
            if rateName == args.rate:
                continue 
            
            altRatesNames.append (rateName)

        self.altRates = []            
        for rateName in altRatesNames:
            self.altRates.append (gfRates.genObject (rateName))
        
        args = self.args 
               
        if args.verbose:            
            print ('Verbose output enabled')
            
            print ('Main rate service: {0}'.format (args.rate))
            print ('Exchanges')
            print ('Origin:            {0}'.format (args.origin))
            print ('Destination:       {0}'.format (args.destination))
            
    def getMainRate (self):
        pass
    
    def getAuxiliaryRate (self):
        pass
    
    def getOriginExchange (self):
        pass
    
    def getDestinationExchange (self):
        pass
    
    def genOutput (self):
        pass

def parseCmdLine ():
    desc = 'Compare two exchanges for a round operation'
    parser = argparse.ArgumentParser (description = desc)
    parser.add_argument ('--rate', '-r', default = 'Google',
                         help = 'Main rate service')
    parser.add_argument ('--origin', '-o', required = True,
                         help = 'Origin exchange')
    parser.add_argument ('--destination', '-d', required = True,
                         help = 'Destination exchange')
    parser.add_argument ('--verbose', '-v', action = "store_true",
                         help = 'Increase output verbosity')
                         
    args = parser.parse_args ()
    
    result = Args ()
    result.rate        = args.rate 
    result.origin      = args.origin 
    result.destination = args.destination 
    
    if args.verbose: 
        print ('Verbose output enabled')
        
        print ('Main rate service: {0}'.format (result.rate))
        print ('Exchanges')
        print ('Origin:            {0}'.format (result.origin))
        print ('Destination:       {0}'.format (result.destination))
    
    # Normal function termination
    return result

def interpretArguments (args):
    pass 

def main (argv):
    app = Application ()
    
    # TODO parse command line 
    app.parseCmdLine ()
    
    # TODO interpret command line 
    # TODO consult main rate service
    # TODO consult auxiliary rate services
    # TODO consult origin exchange 
    # TODO consult destination exchange
    # TODO generate expectations
    # TODO generate output report and JSON files

    # Normal function termination
    return 0

if __name__ == '__main__':
    sys.exit (main (sys.argv))