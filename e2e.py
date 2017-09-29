#! /usr/bin/env python3
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

class Parameters:
    def __init__ (self):
        self.summaryOutput        = None
        self.conclusionOutput     = None
        self.mainRates            = None
        self.altRates             = None
        self.mainRatesOutput      = None
        self.altRatesOutput       = None
        self.origin               = None
        self.destination          = None
        self.originOutputput      = None
        self.destinationOutput    = None
        self.rawOriginOutputput   = None
        self.rawDestinationOutput = None
        self.verbose              = False

    def setSummaryOutput (self, summaryOutput):
        self.summaryOutput = summaryOutput

    def getSummaryOutput (self):
        return self.summaryOutput

    def setConclusionOutput (self, conclusionOutput):
        self.conclusionOutput = conclusionOutput

    def getConclusionOutput (self):
        return self.conclusionOutput

    def setMainRate (self, mainRate):
        self.mainRate = mainRate

    def getMainRate (self):
        return self.mainRate

    def setAltRate (self, altRate):
        self.altRate = altRate

    def getAltRate (self):
        return self.altRate

    def setMainRatesOutput (self, mainRatesOutput):
        self.mainRatesOutput = mainRatesOutput

    def getMainRatesOutput (self):
        return self.mainRatesOutput

    def setAltRatesOutput (self, altRatesOutput):
        self.altRatesOutput = altRatesOutput

    def getAltRatesOutput (self):
        return self.altRatesOutput

    def setOrigin (self, origin):
        self.origin = origin

    def getOrigin (self):
        return self.origin

    def setDestination (self, destination):
        self.destination = destination

    def getDestination (self):
        return self.destination

    def setOriginOutput (self, originOutput ):
        self.originOutput  = originOutput 

    def getOriginOutput (self):
        return self.originOutput 

    def setDestinationOutput (self, destinationOutput):
        self.destinationOutput = destinationOutput 

    def getDestinationOutput (self):
        return self.destinationOutput
        
    def setRawOriginOutput (self, rawOriginOutput):
        self.rawOriginOutput = rawOriginOutput

    def getRawOriginOutput (self):
        return self.rawOriginOutput 

    def setRawDestinationOutput (self, rawDestinationOutput):
        self.rawDestinationOutput = rawDestinationOutput 

    def getRawDestinationOutput (self):
        return self.rawDestinationOutput 

    def setVerbose (self, verbose):
        self.verbose = verbose

    def getVerbose (self):
        return self.verbose
        
class Application:
    def __init__ (self):
        d = datetime.datetime.now ()
        self.suffix = d.strftime ('%Y%m%d_%H%M')
        self.prefix = 'e2e'
    
    def parseCmdLine (self):
        desc = 'Compare two exchanges for a round operation'
        parser = argparse.ArgumentParser (description = desc)
        
        desc = 'Summary report (Default is stdout)' 
        parser.add_argument ('-s', '--summary', required = False,
                             help = desc)
        desc = 'File name for the conclusion of the arbitrage'
        parser.add_argument ('-c', '--conclusion', required = True,
                             help = desc)
        parser.add_argument ('-m', '--main', metavar = "RATES", 
                             default = 'Google',
                             help = 'Main rate service')
        parser.add_argument ('-a', '--alternative', metavar = "RATES",
                             default = 'XRates',
                             help = 'Alternative rate service')
        parser.add_argument ('--origin', '-o', metavar = "EXCHANGE",
                             required = True,
                             help = 'Origin exchange')
        parser.add_argument ('-d', '--destination', metavar = "EXCHANGE",
                             required = True,
                             help = 'Destination exchange')
        parser.add_argument ('-v', '--verbose', action = "store_true",
                             help = 'Increase output verbosity')
                             
        args = parser.parse_args ()
        
        # TODO complete the copy of cmdline parameters
        
        result = Args ()
        result.summary     = args.summary 
        result.conclusion  = args.conclusion 
        result.rates       = args.rates 
        result.alternative = args.alternative 
        result.origin      = args.origin 
        result.destination = args.destination 
        result.verbose     = args.verbose
        
        self.args = result
        
        # Normal function termination
        return result
        
    def interpretArgs (self):
        result = Parameters ()
        
        # Open summary file
        if self.args.summary == None:
            try:
                sum_nam =  self.prefix + '_' + self.suffix + '.sum'
                sum_f = open (sum_nam, 'w')
                
            except IOError:
                # TODO an application specific msg here
                raise
        else:
            sum_f = sys.__stdout__
            
        result.setSummary (sum_f)
            
        # TODO Open output files for destination exchange
        try:
            cnc_nam  =  self.prefix + '_conclusion'
            cnc_nam += '_' + self.suffix + '.json'
            cnc_f = open (cnc_nam, 'w')
            
        except IOError:
            # TODO an application specific msg here
            raise
            
        result.setConclusion (cnc_f)
            
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
        result.setDestination (dstExchange)
            
        # TODO Open output files for destination exchange
        try:
            dst_nam  =  self.prefix + '_' + dstExchange.get_exch_prefix ()
            dst_nam += '_' + self.suffix + '.json'
            e2e_dst_f = open (dst_nam, 'w')
            
        except IOError:
            # TODO an application specific msg here
            raise
            
        result.setDestinationOutput (e2e_dst_f)
            
        try:
            dst_nam  = dstExchange.get_exch_prefix ()
            dst_nam += '_' + self.suffix + '.json'
            dst_f = open (dst_nam, 'w')
            
        except IOError:
            # TODO an application specific msg here
            raise
            
        result.setRawDestinationOutput (dst_f)
            
        # TODO open connection with origin exchange
        orgExchange = gfExchange.genObject (args.origin)
        result.setOrigin (orgExchange)
            
        # TODO Open output files for origin exchange
        try:
            org_nam  =  self.prefix + '_' + orgExchange.get_exch_prefix ()
            org_nam += '_' + self.suffix + '.json'
            e2e_org_f = open (org_nam, 'w')
            
        except IOError:
            # TODO an application specific2 msg here
            raise

        result.setOriginOutput (e2e_org_f)
            
        try:
            org_nam  = orgExchange.get_exch_prefix ()
            org_nam += '_' + self.suffix + '.json'
            org_f = open (org_nam, 'w')
            
        except IOError:
            # TODO an application specific msg here
            raise
            
        result.setRawOriginOutput (org_f)
            
        # TODO open connection with main rate service
        gfRates = gen_factory.GenFactory (rates.Rates)
        rates_names = gfRates.validClassNames ()

        # TODO validate main rate service
        if args.rates not in rates_names:
            fmt  = 'ERROR: Main rates service {0} is not a valid rates name.\n'
            fmt += '\tShould be one of {1}'
            msg = fmt.format (args.rate, rates_names)
            raise Exception (msg)

        mainRates = gfRates.genObject (args.rates)
        result.setMainRates (mainRates)
        
        # TODO Open output file for main rate service
        try:
            rat_nam  =  mainRates.getServicePrefix () + '_'
            rat_nam +=  self.suffix + '.rat'
            rat_f = open (rat_nam, 'w')
            
        except IOError:
            # TODO an application specific msg here
            raise        

        result.setMainRatesOutput (rat_f)
            
        # TODO open connections with auxiliary rate services
        altRatesNames = []        
        for rateName in rates_names:
            if rateName == args.rates:
                continue 
            
            altRatesNames.append (rateName)

        self.altRates = []            
        for rateName in altRatesNames:
            self.altRates.append (gfRates.genObject (rateName))
            
        try:
            altrat_nam  =  'all_rates' + '_'
            altrat_nam +=  self.suffix + '.rat'
            altrat_f = open (altrat_nam, 'w')
            
        except IOError:
            # TODO an application specific msg here
            raise        

        result.setMainRatesOutput (altrat_f)
        
        args = self.args 
               
        if args.verbose:            
            print ('Verbose output enabled')
            
            print ('Main rate service: {0}'.format (args.rates))
            print ('Exchanges')
            print ('Origin:            {0}'.format (args.origin))
            print ('Destination:       {0}'.format (args.destination))
            
    def outMainRates (self):
        pass
    
    def outAlternativeRates (self):
        pass
    
    def outOriginExchange (self):
        pass
    
    def outDestinationExchange (self):
        pass
    
    def genExpectations (self):
        pass
    
    def genOutput (self):
        pass

def main (argv):
    app = Application ()
    
    # TODO parse command line 
    # TODO catch exception
    # TODO return according to error
    app.parseCmdLine ()
    
    # TODO interpret command line 
    # TODO catch exception
    # TODO return according to error
    app.interpretArgs ()
    
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