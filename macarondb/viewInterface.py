#!/usr/bin/python
###############################################################################
#                                                                             #
#    viewInterface.py                                                         #
#                                                                             #
#    Interface for selecting and visualising macaronDB data                   #
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
__copyright__ = "Copyright 2015"
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

# local imports
from dancingPeasant.exceptions import *
from dancingPeasant.interface import Interface
from dancingPeasant.interface import Condition
from view import View
from db import MacaronDB

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class ViewInterface(Interface):
    """Use this interface for visualising data stored in FootballDB DB"""
    def __init__(self,
                 dbFileName,        # file name to connect to
                 verbosity=-1       # turn off all DP chatter
                 ):
        Interface.__init__(self, dbFileName, verbosity)
        self.db = FootballDB(verbosity=verbosity)            # <-- This line is important!
        self.dbFileName = dbFileName
        self.V  = View()
        self.gameStats = ["season","week","opposition","goals",
                          "shotsAttempted","shotsOnTarget","assists",
                          "tackles","intercepts","gkSaves","foulsCommitted",
                          "foulsSuffered","blockedShots","passesAttempted",
                          "passesSuccessful","subbed","attackingPassesAttempted",
                          "attackingPassesSuccessful","turnovers","deflectedPasses"]
    
    #----------------------------------
    
    def viewTable(self,
                  season):
        # view table for specified season
        tableData = {}
        # connect to database
        self.connect()
        
        # set the select condition
        C = Condition("season", "=", season)
        
        # access the database and get rows
        rows = self.select('results', ["week","team_a","team_b","score_a","score_b"], C)
        
        # disconnect once done
        self.disconnect()
        
        for row in rows:
            week    = int(row[0])
            team_a  = row[1]
            team_b  = row[2]
            score_a = row[3]
            score_b = row[4]
            
            # initialise team
            self.initialiseTeam(tableData,team_a)
            self.initialiseTeam(tableData,team_b)
            
            # add data to dictionary
            self.prepareData(tableData, team_a, team_b, score_a, score_b)
            
        sorted_table = sorted(tableData.items(), key=lambda x:x[1]['points'],reverse=True)
        
        self.V.visualiseTable(sorted_table,tableData, season)
            
    def initialiseTeam(self, tableData, team):
        if team not in tableData and team!= 'bye':
            tableData[team] = {}
            tableData[team]['goalsFor']         = 0
            tableData[team]['goalsAgainst']     = 0
            tableData[team]['wins']             = 0
            tableData[team]['losses']           = 0
            tableData[team]['draws']            = 0
            tableData[team]['byes']             = 0
            tableData[team]['forfeitWins']      = 0
            tableData[team]['forfeitLosses']    = 0
            tableData[team]['points']           = 0
            tableData[team]['bonusPoints']      = 0
    
    def prepareData(self, tableData, team_a, team_b, score_a, score_b):
        # check if bye
        if self.isBye(team_a,team_b):
            if team_a == 'bye':
                self.addDataToTable(tableData,
                                    team_b,
                                    goalsFor=0,
                                    goalsAgainst=0,
                                    wins=0,
                                    losses=0,
                                    draws=0,
                                    byes=1,
                                    forfeitWins=0,
                                    forfeitLosses=0,
                                    points=0,
                                    bonusPoints=0)
            elif team_b == 'bye':
                self.addDataToTable(tableData,
                                    team_a,
                                    goalsFor=0,
                                    goalsAgainst=0,
                                    wins=0,
                                    losses=0,
                                    draws=0,
                                    byes=1,
                                    forfeitWins=0,
                                    forfeitLosses=0,
                                    points=0,
                                    bonusPoints=0)
        
        # check if forfeit
        elif self.isForfeit(score_a, score_b):
            if score_a == 'FW':
                self.addDataToTable(tableData,
                                    team_a,
                                    goalsFor=0,
                                    goalsAgainst=0,
                                    wins=0,
                                    losses=0,
                                    draws=0,
                                    byes=0,
                                    forfeitWins=1,
                                    forfeitLosses=0,
                                    points=4,
                                    bonusPoints=0)
                self.addDataToTable(tableData,
                                    team_b,
                                    goalsFor=0,
                                    goalsAgainst=0,
                                    wins=0,
                                    losses=0,
                                    draws=0,
                                    byes=0,
                                    forfeitWins=0,
                                    forfeitLosses=1,
                                    points=0,
                                    bonusPoints=0)
            elif score_b == 'FW':
                self.addDataToTable(tableData,
                                    team_b,
                                    goalsFor=0,
                                    goalsAgainst=0,
                                    wins=0,
                                    losses=0,
                                    draws=0,
                                    byes=0,
                                    forfeitWins=1,
                                    forfeitLosses=0,
                                    points=4,
                                    bonusPoints=0)
                self.addDataToTable(tableData,
                                    team_a,
                                    goalsFor=0,
                                    goalsAgainst=0,
                                    wins=0,
                                    losses=0,
                                    draws=0,
                                    byes=0,
                                    forfeitWins=0,
                                    forfeitLosses=1,
                                    points=0,
                                    bonusPoints=0)
        
        # check if grading game
        # needs some work
        
        # check if result
        else:
            result  = self.gameResult(score_a,score_b)
            bonus   = self.gameBonus(score_a,score_b)
            score_a = int(score_a)
            score_b = int(score_b)
            
            if result == 'draw':
                self.addDataToTable(tableData,
                                    team_a,
                                    goalsFor=score_a,
                                    goalsAgainst=score_b,
                                    wins=0,
                                    losses=0,
                                    draws=1,
                                    byes=0,
                                    forfeitWins=0,
                                    forfeitLosses=0,
                                    points=2+bonus[0],
                                    bonusPoints=bonus[0])
                self.addDataToTable(tableData,
                                    team_b,
                                    goalsFor=score_b,
                                    goalsAgainst=score_a,
                                    wins=0,
                                    losses=0,
                                    draws=1,
                                    byes=0,
                                    forfeitWins=0,
                                    forfeitLosses=0,
                                    points=2+bonus[1],
                                    bonusPoints=bonus[1])
            elif result == 'awin':
                self.addDataToTable(tableData,
                                    team_a,
                                    goalsFor=score_a,
                                    goalsAgainst=score_b,
                                    wins=1,
                                    losses=0,
                                    draws=0,
                                    byes=0,
                                    forfeitWins=0,
                                    forfeitLosses=0,
                                    points=4+bonus[0],
                                    bonusPoints=bonus[0])
                self.addDataToTable(tableData,
                                    team_b,
                                    goalsFor=score_b,
                                    goalsAgainst=score_a,
                                    wins=0,
                                    losses=1,
                                    draws=0,
                                    byes=0,
                                    forfeitWins=0,
                                    forfeitLosses=0,
                                    points=0+bonus[1],
                                    bonusPoints=bonus[1])
            elif result == 'bwin':
                self.addDataToTable(tableData,
                                    team_a,
                                    goalsFor=score_a,
                                    goalsAgainst=score_b,
                                    wins=0,
                                    losses=1,
                                    draws=0,
                                    byes=0,
                                    forfeitWins=0,
                                    forfeitLosses=0,
                                    points=0+bonus[0],
                                    bonusPoints=bonus[0])
                self.addDataToTable(tableData,
                                    team_b,
                                    goalsFor=score_b,
                                    goalsAgainst=score_a,
                                    wins=1,
                                    losses=0,
                                    draws=0,
                                    byes=0,
                                    forfeitWins=0,
                                    forfeitLosses=0,
                                    points=4+bonus[1],
                                    bonusPoints=bonus[1])
            
    def addDataToTable(self, tableData, team, goalsFor, goalsAgainst,
                       wins, losses, draws, byes, forfeitWins,
                       forfeitLosses, points, bonusPoints):
        tableData[team]['goalsFor']         += goalsFor
        tableData[team]['goalsAgainst']     += goalsAgainst
        tableData[team]['wins']             += wins
        tableData[team]['losses']           += losses
        tableData[team]['draws']            += draws
        tableData[team]['byes']             += byes
        tableData[team]['forfeitWins']      += forfeitWins
        tableData[team]['forfeitLosses']    += forfeitLosses
        tableData[team]['points']           += points
        tableData[team]['bonusPoints']      += bonusPoints
    
    def isGrading(self,
                  score_a,
                  score_b):
        if score_a == 'GW' or score_b == 'GW':
            return True
    
    def isBye(self,
              team_a,
              team_b
              ):
        if team_a == 'bye' or team_b == 'bye':
            return True
    
    def isForfeit(self,
                  score_a,
                  score_b
                  ):
        if score_a == 'FW' or score_a == 'FL' or score_b == 'FW' or score_b == 'FL':
            return True
        
    def gameBonus(self,
                  score_a,
                  score_b):
        bonus_a = score_a / 3
        bonus_b = score_b / 3
        return [bonus_a, bonus_b]
    
    def gameResult(self,
                   score_a,
                   score_b):
        if score_a == score_b:
            return 'draw'
        elif score_a > score_b:
            return 'awin'
        elif score_a < score_b:
            return 'bwin'
    
    #----------------------------------
    def viewPlayerStat(self,
                       player,
                       stat):
        # local variables
        playerData = {}
        
        # connect to database
        self.connect()
        
        # set condition for select statement
        rows = self.select(player, ["season","week","opposition","goals",
                                    "shotsAttempted","shotsOnTarget","assists",
                                    "tackles","intercepts","gkSaves","foulsCommitted",
                                    "foulsSuffered","blockedShots","passesAttempted",
                                    "passesSuccessful","subbed","attackingPassesAttempted",
                                    "attackingPassesSuccessful","turnovers","deflectedPasses"])
        
        # disconnect from db
        self.disconnect()
        
        # collect db data
        for row in rows:
            season  = row[0]
            week    = row[1]
            self.addPlayerDataAllWrapper(playerData, season, week, row)
            
        # ordered dict
        sortedPlayerData = sorted(playerData.items(), key=lambda x:x[1],reverse=True)
        
        # visualise player data
        self.V.visualisePlayerStats(playerData,
                                    sortedPlayerData,
                                    stat)

    #----------------------------------
    def viewPlayerSummary(self, player):
        # local variables
        playerData = {}
        
        # connect to db
        self.connect()
        
        # set condition for select statement
        rows = self.select(player, ["season","week","opposition","goals",
                                    "shotsAttempted","shotsOnTarget","assists",
                                    "tackles","intercepts","gkSaves","foulsCommitted",
                                    "foulsSuffered","blockedShots","passesAttempted",
                                    "passesSuccessful","subbed","attackingPassesAttempted",
                                    "attackingPassesSuccessful","turnovers","deflectedPasses"])
        
        # disconnect from db
        self.disconnect()
        
        # collect db data
        for row in rows:
            season  = row[0]
            week    = row[1]
            self.addPlayerDataAllWrapper(playerData, season, week, row)
            
        # ordered dict
        sortedPlayerData = sorted(playerData.items(), key=lambda x:x[1],reverse=True)
        
        self.V.visualisePlayerSummary(playerData,
                                    sortedPlayerData,
                                    stat)
 
    #------------------------------------
    #         Univeral functions        #
    #------------------------------------
    def addPlayerDataAllWrapper(self, playerData, season, week, row):
        
        for i,data in enumerate(row[2:]):    
            statName    = self.gameStats[i+2]
            statValue   = data
            self.addPlayerDataAll(playerData,
                                  season,
                                  week,
                                  statName,
                                  statValue)
        
    def addPlayerDataAll(self, playerData, season, week, statName, statValue):
        try:
            playerData[season][week][statName] = statValue
        except KeyError:
            try:
                playerData[season][week] = {statName:statValue}
            except KeyError:
                playerData[season] = {week:{statName:statValue}}
        
    
        
    
