#!/usr/bin/python
###############################################################################
#                                                                             #
#    importInterface.py                                                       #
#                                                                             #
#    Interface for importing data stored in csv files into the macaronDB      #
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
import sqlite3 as lite
import operator
from datetime import datetime

# local imports
from dancingPeasant.exceptions import *
from dancingPeasant.interface import Interface
from dancingPeasant.interface import Condition
from db import MacaronDB

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class ImportInterface(Interface):
    """Use this interface for importing data stored in csv
    files into the FootballDB DB"""
    def __init__(self,
                 dbFileName,        # file name to connect to
                 verbosity=-1       # turn off all DP chatter
                 ):
        Interface.__init__(self, dbFileName, verbosity)
        self.db = MacaronDB(verbosity=verbosity)            # <-- This line is important!
        self.dbFileName = dbFileName
    
    def createDatabase(self, ):
        if not self.connect(createDB=True):
            # database exists
            pass
        else:
            # if True, database has been created!
            print "Database %s created" % self.dbFileName
    
        self.disconnect()
    
    def importIngredientPrices(self,
                               ingredientPricesFile):
        if not self.connect(createDB=True):
            # database exists
            pass
        else:
            # if True, database has been created!
            print "Database %s created" % self.dbFileName
        
        table_name = 'ingredient_prices'
        
        # Check if ingredients table exists, if not, create!
        self.checkTableExists(table_name)
        self.addIngredientPrices(table_name,
                                 ingredientPricesFile)
    
    def addIngredientPrices(self,
                            table_name,
                            ingredientPricesFile):
        """Add/update ingredients table"""
        
        # get current time
        date = str(datetime.now())
        
        with open(ingredientPricesFile) as fh:
            line_number = 0
            for l in fh:
                commas = l.rstrip().split(",")
                if line_number > 0: # skips header line
                    ingredient  = commas[0]
                    volume      = commas[1]
                    price       = commas[2]
                    to_db = [(ingredient, volume, price, date)]
                    self.insert(table_name,
                                ["ingredient",
                                 "volume",
                                 "price",
                                 "date"],
                                to_db)
                line_number += 1
                
        self.disconnect()
    
    def checkTableExists(self,
                         table):
        try:
            table_data = self.select(table, "*")
            print "%s exists, updating" % table
            return True
        except(lite.OperationalError):
            self.db.addNewTable(table)
            print "Added new table called %s" % table
    
    def importGameStats(self,
                       gameDataCSV,     # file containing data 
                       opposition,      # string of opposition team
                       season,          # int of season number
                       week):           # int of week in season
        """import new game data into the FootballDB
           Create new DB if it doesn't exist!"""
         
        if not self.connect(createDB=True):
            # database exists
            pass
        else:
            # if True, database has been created!
            print "Database %s created" % self.dbFileName
        
        # add game data to DB
        self.convertFileIntoArray(gameDataCSV,
                                opposition,
                                season,
                                week
                                )
        
        self.disconnect()
    
    def convertFileIntoArray(self,
                             gameDataCSV,
                             opposition,
                             season,
                             week
                             ):
        
        with open(gameDataCSV) as fh:
            for l in fh:
                commas = l.rstrip().split(",")
                
                # skip header
                if commas[0].lower() != 'player':
                    player                      = commas[0]
                    goals                       = commas[1]
                    shotsAttempted              = commas[2]
                    shotsOnTarget               = commas[3]
                    assists                     = commas[4]
                    tackles                     = commas[5]
                    intercepts                  = commas[6]
                    gkSaves                     = commas[7]
                    foulsCommitted              = commas[8]
                    foulsSuffered               = commas[9]
                    blockedShots                = commas[10]
                    passesAttempted             = commas[11]
                    passesSuccessful            = commas[12]
                    subbed                      = commas[13]
                    attackingPassesAttempted    = commas[14]
                    attackingPassesSuccessful   = commas[15]
                    turnovers                   = commas[16]
                    deflectedPasses             = commas[17]

                    to_db = [(season, week, opposition, goals,shotsAttempted,shotsOnTarget,assists,tackles,
                            intercepts,gkSaves,foulsCommitted,foulsSuffered,
                            blockedShots,passesAttempted,passesSuccessful,subbed,
                            attackingPassesAttempted,attackingPassesSuccessful,turnovers,deflectedPasses)]
                    
                    # check to see if table exists, if not, create it!
                    #self.db.addNewPlayer(player)
                    if self.doesPlayerTableExist(player):
                        if self.doesGameDataExist(player, season, week):
                            # insert data into table
                            self.insert(player,
                                        [
                                        "season","week","opposition","goals","shotsAttempted",
                                        "shotsOnTarget","assists","tackles","intercepts",
                                        "gkSaves","foulsCommitted","foulsSuffered",
                                        "blockedShots","passesAttempted","passesSuccessful",
                                        "subbed","attackingPassesAttempted","attackingPassesSuccessful",
                                        "turnovers","deflectedPasses"
                                        ],
                                        to_db)
                    else:
                        print "Adding new player (%s) table to %s" % (player, self.dbFileName)
                         # create table
                        self.db.addNewPlayer(player)
                        
                        # then add data
                        self.insert(player,
                                    [
                                    "season","week","opposition","goals","shotsAttempted",
                                    "shotsOnTarget","assists","tackles","intercepts",
                                    "gkSaves","foulsCommitted","foulsSuffered",
                                    "blockedShots","passesAttempted","passesSuccessful",
                                    "subbed","attackingPassesAttempted","attackingPassesSuccessful",
                                    "turnovers","deflectedPasses"
                                    ],
                                    to_db)
                    
    def doesGameDataExist(self, player, season, week):
        try:
            C = Condition("season", "=", season)
            bc = Condition("week", "=", week)
            C = Condition(C, "and", bc)
            gameData = self.select(player, ["*"], C)
            if len(gameData) == 0:
                return True
            else:
                print "ImportError: game data already exists for season %d week %d" % (season, week)
                sys.exit()
        except(lite.OperationalError):
            return True
    
    def doesPlayerTableExist(self, player):
        try:
            table_data = self.select(player, "*")
            return True
        except(lite.OperationalError):
            return False

    def insertData(self, ):
        pass
    
    
    def importResults(self,
                      resultsDataFile,
                      season,
                      week
                      ):
        """Import the results for the round into the ladder DB.
           Create new database if it doesn't already exist!"""
        
        if not self.connect(createDB=True):
            # database exists
            pass
        else:
            # if True, database has been created!
            print "Database %s created" % self.dbFileName
    
        # add round results to DB
        self.addRoundResults(resultsDataFile,
                             season,
                             week)
        
        self.disconnect()
    
    
    def addRoundResults(self,
                        resultsDataFile,
                        season,
                        week):
        # table already exists, created with the database!
        with open(resultsDataFile) as fh:
            for l in fh:
                commas        = l.rstrip().split(",")
                team_a      = commas[0]
                team_b      = commas[1]
                score_a     = commas[2]
                score_b     = commas[3]
                
                to_db = [(season, week, team_a, team_b, score_a, score_b)]
        
                self.insert('results',
                            [
                             "season",
                             "week",
                             "team_a",
                             "team_b",
                             "score_a",
                             "score_b"
                             ],
                            to_db)
                
    def addBars(self):
        """Add bars to the database"""
        if not self.connect(createDB=True):
            # database exists
            pass
        else:
            # if True, database has been created!
            print "Database %s created" % self.dbFileName
        
        # connect to the database
        #self.connect()
    
        # bars is an array of tuples. All ordered in the same way
        # EX:
        bars =  [(10, 1, "iron"), (20, 15, "wax")]
        #bars =  [(1, 15, "gold"), (2, 15, "asphalt")]
        #
        self.insert("bars",
                    ["length",
                     "diameter",
                     "material"],
                     bars)
    
        # disconnect once done
        self.disconnect()
    
    def getBars(self, length):
        """Get bars longer than a set length"""
    
        # connect to the database
        self.connect()
    
        # set the select condition
        C = Condition("length", ">", length)
    
        # access the database and get rows
        rows = self.select('bars', ["material", "diameter"], C)
    
        # disconnect once done
        self.disconnect()
    
        # do something with the results