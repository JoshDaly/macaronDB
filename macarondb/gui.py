#!/usr/bin/env python
###############################################################################
#                                                                             #
#    gui.py                                                                   #
#                                                                             #
#    Handles all graphical user interface                                     #
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
import os

# local imports
from importInterface import ImportInterface
from viewInterface import ViewInterface
from tkinter import *
import tkMessageBox
import tkFileDialog
from dancingPeasant.exceptions import *
from dancingPeasant.interface import Interface
from dancingPeasant.interface import Condition
from db import MacaronDB

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class GraphicalUserInterface(Interface):
    def __init__(self,):
        pass
    
    def initialiseDatabase(self,
                           dbFileName,        # db file name
                            verbosity=-1       # turn off all DP chatter
                           ):
        Interface.__init__(self, dbFileName, verbosity)
        self.db = MacaronDB(verbosity=verbosity)            # <-- This line is important!
        self.dbFileName = dbFileName
    
    def hello(self, ):
        print "Hello!"
    
    def GraphicalUserInterface(self, ):
        # create root window object
        root = self.createGUI()
        
        # create menu object
        menubar = Menu(root)
        
        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Import Database", command=lambda: self.importDatabase(root))
        filemenu.add_command(label="New", command=lambda: self.createNewDatabase(root))
        filemenu.add_command(label="Save", command=self.hello)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=lambda: self.aboutHelpText(root))
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        # display the menu
        root.config(menu=menubar)
        
        root.mainloop()
    
    def importDatabase(self,
                       root):
        # create new window
        current_window = Toplevel(root)
        
        
    
    
    def createNewDatabase(self,
                          root):
        """Create new database file"""
        # create entry point for database name
        # create new window
        current_window = Toplevel(root)
        
        Label1 = Label(current_window, text="Database Name")
        Label1.grid(row=0)
        Label2 = Label(current_window, text="Directory")
        Label2.grid(row=1)
        Entry1 = Entry(current_window, bd = 5)
        Entry1.grid(row=0,column=1)
        Entry2 = Entry(current_window, bd = 5)
        Entry2.grid(row=1, column=1)

        # create buttons for handling input
        Button1 = Button(current_window, text='Choose directory',command=lambda: self.askdirectory(Entry2))
        Button1.grid(row=1,column=2,sticky='nsew',pady=4)
        
        Button2 = Button(current_window, text='Create', command=lambda: self.createDatabaseFromName(current_window, Entry1, Entry2))
        Button2.grid(row=2, column=1, sticky='nsew', pady=4)
        
        Button3 = Button(current_window, text='Cancel',command=lambda: self.closeTopLevelWindow(current_window))
        Button3.grid(row=2,column=0,sticky='nsew', pady=4)
    
    def askdirectory(self,
                     entry):
        dirname = tkFileDialog.askdirectory()
        entry.insert(0,dirname)
        return
    
    def test(self,
             function):
        
        if function == 'gui':
            self.testGraphicalUserInterface()
            
        elif function == 'create':
            self.createDatabase()
    
    def closeTopLevelWindow(self,
                    current_window):
        current_window.destroy()
    
    def createDatabaseFromName(self,
                               current_window,
                               dbFileName,
                               directory
                               ):
        dbFileName = os.path.join(directory.get(), dbFileName.get())
        tkMessageBox.showinfo("Attention","Created new database called %s" % dbFileName)
        
        # get an interface to the file
        II = ImportInterface(dbFileName)
        II.createDatabase()
        
        self.closeTopLevelWindow(current_window)
    
    def testGraphicalUserInterface(self, ):
        """Non-specific GUI testing"""
        # create root window object
        self.createGUI()
        
        # set title
        root.title("MacaronDB %s" % __version__)
        
        # set size parameters
        root.geometry("800x600")
        
        # create label
        app = Frame(root)
        app.grid()
        loaded_database = self.dbFileName.split("/")[-1]
        label = Label(app, text="Loaded Database: %s" % loaded_database)
        
        # visualise label
        label.grid()
        
        # run gui
        root.mainloop()

    def createGUI(self, ):
        # create GUI
        root = Tk()
        # set size parameters
        root.geometry("400x400")
        # set title
        root.title("MacaronDB %s" % __version__)
        
        return root
    
    def aboutHelpText(self,
                      root
                      ):
        S = Scrollbar(root)
        T = Text(root, height=4, width=400)
        S.pack(side=RIGHT,fill=Y)
        T.pack(side=LEFT,fill=Y)
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        quote="""\
             ...::: MacaronDB :::...

    Store all your macaron data in a handy SQLite database

    -----------------------------------------
                   version: %s
    -----------------------------------------

        """ % __version__
        T.insert(END, quote)
        
        