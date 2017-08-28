#!/usr/bin/python
###############################################################################
#                                                                             #
#    server.py                                                                #
#                                                                             #
#    Main entry point for the macaronDB software                              #
#                                                                             #
#    Copyright (C) Joshua Daly                                                #
#                                                                             #
###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

__author__ = "Joshua Daly"
__copyright__ = "Copyright 2017"
__credits__ = ["Joshua Daly"]
__license__ = "GPLv3"
__version__ = "0.1.0"
__maintainer__ = "Joshua Daly"
__email__ = "joshua.daly@uqconnect.edu.au"
__status__ = "Dev"

###############################################################################
###############################################################################
###############################################################################
###############################################################################

# system imports
import sys

# local imports
from importInterface import ImportInterface
from viewInterface import ViewInterface

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class Server(object):
    def __init__(self,
                 dbfilename         # path to db file to work with
                 ):
        self.dbfilename = dbfilename
    
    def sayHi(self,):
    	print "Successfully imported server"
    
    def importGameStats(self,
                        gameStatsFile,  # csv containing game statistics
                        opposition,     # opposition team name
                        season,         # season number
                        week            # week number
                        ):
        print "Importing new game data for Week %d of Season %d against %s" % (week,
                                                                               season,
                                                                               opposition)
        # get an interface to the file
        II = ImportInterface(self.dbfilename)
        
        # import game stats as csv file
        II.importGameStats(gameStatsFile,
                          opposition,
                          season,
                          week)
    
    def importResults(self,
                      resultsDataFile,
                      season,
                      week):
        print "Importing round results for Week %d of Season %d" % (week,
                                                                    season)
        # get an interface to the file
        II = ImportInterface(self.dbfilename)
        
        # import results as csv file
        II.importResults(resultsDataFile,
                         season,
                         week)
    
    def viewTable(self,
                  season):
        # get an interface to the file
        VI = ViewInterface(self.dbfilename)
        
        VI.viewTable(season)
    
    def viewTeam(self):
        """TBC"""
        pass
    
    def viewPlayerStat(self,
                        player,
                        stat):
        # get an interface to the file
        VI = ViewInterface(self.dbfilename)
        
        # visualise player data
        VI.viewPlayerStat(player,
                        stat)
    
    def viewPlayerSummary(self,
                          player):
        # get an interface to the db file
        VI = ViewInterface(self.dbfilename)
        
        # visualise player summary
        VI.viewPlayerSummary(player)    
    
    def viewCompare(self):
        """TBC"""
        pass
    
    def importTest(self):
        # get an interface to the file
        II = ImportInterface(self.dbfilename)
        
        II.addBars()