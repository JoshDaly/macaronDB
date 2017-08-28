#!/usr/bin/python
###############################################################################
#                                                                             #
#    view.py                                                                  #
#                                                                             #
#    suite of visualisations available for macaronDB                          #
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
import numpy as np
import matplotlib.pyplot as plt

# local imports

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class View(object):
    def __init__(self):
        pass
    
    #----------------------------------------
    
    def visualisePlayerStats(self,
                             playerData,
                             sortedPlayerData,
                             stat):
        """
        "season","week","opposition","goals",
        "shotsAttempted","shotsOnTarget","assists",
        "tackles","intercepts","gkSaves","foulsCommitted",
        "foulsSuffered","blockedShots","passesAttempted",
        "passesSuccessful","subbed","attackingPassesAttempted",
        "attackingPassesSuccessful","turnovers","deflectedPasses"
        """
        if(stat == "goals" or stat == "assists" or stat == "tackles" or
           stat == "intercepts" or stat == "gkSaves" or stat == "blockedShots" or
           stat == "subbed" or stat == "turnovers" or stat == "deflectedPasses"):
            # make bar chart with matplotlib 
            fig = plt.figure()
            ax  = plt.subplot(1,1,1)
            
            # calculate the number of data points
            ind, ys = self.numDataPoints(playerData,
                                        sortedPlayerData)
            
            self.barChart(ind,
                          ys)
        
        elif stat == 'passPercentage':
            # make pie chart with matplotlib
            # set variables to zero
            passesAttempted     = 0
            passesSuccessful    = 0
            
            for data in sortedPlayerData:
                season = data[0]
                for week in data[1].keys():
                    passesAttempted     += int(data[1][week]['passesAttempted'])
                    passesSuccessful    += int(data[1][week]['passesSuccessful'])
                    
            percSuccessful      = float(passesSuccessful)/passesAttempted * 100
            percUnSuccessful    = float(passesAttempted - passesSuccessful)/passesAttempted * 100
            
            labels = ['passesSuccessful','passesUnSuccessful']
            
            sizes  = [percSuccessful,percUnSuccessful]
            
            self.pieChart(labels, sizes)
        
        elif stat == 'attackingPassPercentage':
            # make pie chart with matplotlib 
                        # set variables to zero
            attackingPassesAttempted     = 0
            attackingPassesSuccessful    = 0
            
            for data in sortedPlayerData:
                season = data[0]
                for week in data[1].keys():
                    attackingPassesAttempted     += int(data[1][week]['attackingPassesAttempted'])
                    attackingPassesSuccessful    += int(data[1][week]['attackingPassesSuccessful'])
                    
            percSuccessful      = float(attackingPassesSuccessful)/attackingPassesAttempted * 100
            percUnSuccessful    = float(attackingPassesAttempted - attackingPassesSuccessful)/attackingPassesAttempted * 100
            
            labels = ['attackingPassesSuccessful','passesUnSuccessful']
            
            sizes  = [percSuccessful,percUnSuccessful]
            
            self.pieChart(labels, sizes)    
        
        elif stat == 'shotPercentage':
            # make pie chart with matplotlib 
            pass
    
    def barChart(self,
                 independentVariables,
                 yDataPoints):
        
        ax.bar(independentVariables, yDataPoints, 0.35)
        plt.show()
    
    def pieChart(self, labels, sizes):
        # set colour blind safe colour scheme
        colours = ["#1f78b4","#a6cee3"]
        
        explode = (0.1,0) # explode the first slice
        
        plt.pie(sizes, explode=explode, labels=labels, colors=colours,autopct='%1.1f%%', shadow=True, startangle=90)
    
        plt.axis('equal')
        
        plt.show()
        
        
    def numDataPoints(self,
                      playerData,
                      sortedPlayerData):
        N  = 0
        ys = []
        for data in sortedPlayerData:
            season = data[0]
            N += len(playerData[season])
            for week in data[1].keys():
                stat = data[1][week]
                ys.append(stat)
        ind = np.arange(N)
        return ind, ys
    
    #----------------------------------------
    
    def visualisePlayerSummary(self, ):
        pass
    
    #----------------------------------------
    
    def visualiseTeamStats(self):
        pass
    
    #----------------------------------------
    
    def compareStats(self, type, ):
        pass
    
    #----------------------------------------
    
    def visualiseTable(self, orderedTable, tableData, season):
        """visualise table using blank scatter plot"""
        fig     = plt.figure(figsize=(8, 2),dpi=400)
        ax      = plt.subplot(1,1,1)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        tableHeaders = ['teams','wins', 'draws', 'losses',
                        'goalsFor','goalsAgainst',
                        'byes','forfeitWins',
                        'forfeitLosses','points',
                        'bonusPoints']
        
        data = []
        
        # print header
        header_to_print = "\t".join(tableHeaders)
        print "###########################################################"
        print "-----------Brisbane City Indoor Sports Season %d-----------" % season
        print "###########################################################"
        print header_to_print
        
        # print table
        for team in orderedTable:
            array = [team[0]]
            data_to_print = team[0]
            for header in tableHeaders[1:]:
                #array.append(tableData[team[0]][header])
                data_to_print += "\t%s" % str(tableData[team[0]][header])
            data.append(array)
            print data_to_print
        
        print "###########################################################"
        print "###########################################################"
        
        # Need to find better table out format
        #table = ax.table(cellText=data,
        #                 colLabels=tableHeaders,
        #                 loc='center'
        #                 )
        
        #plt.savefig('tmp', type='png')
        
    #----------------------------------------
        
        
    
    