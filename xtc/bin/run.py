#!/usr/bin/python3

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
import sys
import os
import logging
import runui
import common
import connectThread
import dialoglogin

class runUI(QtWidgets.QMainWindow, runui.Ui_run):

    def __init__(self, connectionname):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        values = common.readConnection(connectionname)
        self.connectionExec(values)
    
    #def closeEvent(self, event):
    #    logging.info("close")
    #    sys.exit(0)

    # called by threadConnect when connection end
    def connectThreadCancel(self):
        self.runconnect.terminate()
        #sys.exit(0)
        self.close()

    def connectionExec(self, values):
        # logging
        configfile = common.ressourcefile
        loggingfilename = common.getRessourceByName(configfile, "loggingFileRun")
        debugfile = common.getRessourceByName(configfile, "debugSwitch")
        debug = False
        if os.path.isfile(debugfile):
            debug = True
        common.loggingStart(loggingfilename, debug)
        logging.info("connectionExec")
        
        run = 0
        while run < 2:
            connectionname = values["name"]
            command = values["command"]
            systemlogin = values["systemlogin"]
            logging.info("connectionExec " + connectionname)
            
            result = True            
            if systemlogin == "yes":
                common.runProgram(common.getRessource("commandWMDesktop"))
                logging.info("loginDialog")
                dialogLogin = dialoglogin.dialogLoginUI(configfile, connectionname)
                dialogLogin.exec_()
                result = dialogLogin.getResult()
                if result is True:
                    # replace parameter <user> and <password> in command string
                    command = command.replace(common.getRessource("commandPlaceholderUser"), dialogLogin.getLogin())
                    command = command.replace(common.getRessource("commandPlaceholderPassword"), dialogLogin.getPassword())
                    
            if result:
                result = common.isHostAlive(values["address"])
        
            if result:
                break
            else:
                if "alternative" in values:
                    if values["alternative"] != "":
                        alternative = values["alternative"]
                        values = []
                        values = common.readConnection(alternative)
                        if not "name" in values:
                            break;
                    else:
                        break
                else:
                    break
            run = run + 1
                       
        if result:            
            # connect to Desktop 1
            commandwm = common.getRessource("commandWMDesktop")
            command = commandwm + " " + command
            logging.info(command)
            # run connection as thread
            self.runconnect = connectThread.connectThread(command, connectionname)
            self.runconnect.threadCancel.connect(self.connectThreadCancel)
            self.runconnect.start()
        else:
            common.messageDialog("runNoConnection")
            self.close()
            #sys.exit(1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = runUI(sys.argv[1])
    #form.show()
    app.exec_()
