from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import common
import connectThread
import dialoglogin
import logging
import os
import shutil

def autostartvpn(self, ovpn, parameter, systemlogin):
    logging.info("autostartvpn")
    vpnExec(self, ovpn, parameter, systemlogin)

        
def vpnExec(self, ovpn, parameter, systemlogin):
    command = common.getRessource("commandVPNExec")
    command = command + " " + ovpn
    command = command + " " + common.getRessource("commandVPNLog")
    if parameter != None:
        command = command + " \"" + parameter  + "\""
    result = True
    if systemlogin == "yes":
        needinput = True
        while needinput:
            dialogLogin = dialoglogin.dialogLoginUI(self.configfile, "VPN")
            dialogLogin.exec_()
            result = dialogLogin.getResult()
            if result is True:
                if dialogLogin.getLogin() != "" and dialogLogin.getPassword() != "":
                    command = command + " " + dialogLogin.getLogin()
                    command = command + " \'" + dialogLogin.getPassword() + "\'"
                    needinput = False
            else:
                break
    logging.info(command)
    
    if result:
        # run connection as thread
        connectionlog = common.getRessource("fileConnectionLog")
        runconnect = connectThread.connectThread(command, "vpn", connectionlog)
        runconnect.threadCancel.connect(self.connectThreadCancel)
        self.connectedThreads["vpn"] = runconnect
        runconnect.start()
        if vpnCheckState():
            self.vpnButtonConnect.setEnabled(False)
            self.vpnButtonCondition.setIcon(QtGui.QIcon(common.getRessource("connectIcon")))


def vpnCheckState():
    command = common.getRessource("commandVPNState")
    command = command + " " + common.getRessource("commandVPNLog")
    logging.info(command)
    return common.runProgram(command)
    
    
# Button Transfer
def vpnTransfer(self):
    logging.info("vpnTransfer")
    values = {}
    values["ovpn"] = self.vpnInputovpn.text()
    values["parametervpn"] = self.vpnInputParameter.text()
    values["autostartvpn"] = "no" 
    if self.vpnInputAutostart.isChecked():
        values["autostartvpn"] = "yes"
    values["systemlogin"] = "no" 
    if self.vpnInputSystemLogin.isChecked():
        values["systemlogin"] = "yes"
    writeVPN(values)
    
    
# Button Connect
def vpnConnect(self):
    logging.info("vpnConnect")
    ovpn = self.vpnInputovpn.text()
    parameter = self.vpnInputParameter.text()        
    systemlogin = "no"
    if self.vpnInputSystemLogin.isChecked():
        systemlogin = "yes"        
    vpnExec(self, ovpn, parameter, systemlogin)    
    
        
# Button Cancel
def vpnCancel(self):
    logging.info("vpnCancel")
    command = common.getRessource("commandVPNKill") 
    command = command + " " + common.getRessource("commandVPNLog") 
    logging.info(command)
    common.runProgram(command)    
    self.vpnButtonConnect.setEnabled(True)
    self.vpnButtonCondition.setIcon(QtGui.QIcon(common.getRessource("disconnectIcon")))
    
        
# Button Condition
def vpnCondition(self):
    logging.info("vpnCondition")
       
    try:
        fileout = common.getRessource("commandVPNLog")
        filer = open(fileout, "r")            
        text = filer.read()            
        filer.close()
        common.textDialog("VPN", text)
    except OSError as error:
        pass        
    

def vpnGetFile(self):
    logging.info("vpnGetFile")
    command = common.getRessource("commandMountUSB") 
    logging.info(command)
    common.runProgram(command, False)
    filename = getFile("ovpn", common.getRessource("VPNUSBDirectory"))
    if filename != "":
        targetfilename = common.getRessource("VPNOvpnFile")
        command = common.getRessource("commandVPNCopy") + " " + filename + " " + targetfilename
        logging.info(command)
        common.runProgram(command)
        self.vpnInputovpn.setText(targetfilename)
    command = common.getRessource("commandUmountUSB") 
    logging.info(command)
    common.runProgram(command, False)
   
         
def vpnAdditionalFiles(self):
    logging.info("vpnAdditionalFiles")
    command = common.getRessource("commandMountUSB") 
    logging.info(command)
    common.runProgram(command, False)
    filename = getFile(None, common.getRessource("VPNUSBDirectory"))
    if filename != "":
        command = common.getRessource("commandVPNCopy") + " " + filename
        logging.info(command)
        common.runProgram(command, False)
    command = common.getRessource("commandUmountUSB") 
    logging.info(command)
    common.runProgram(command, False)


def vpnDeleteFile(self):
    logging.info("vpnDeleteFile")
    directory = common.getRessource("VPNDirectory")
    filename = getFile(None, directory)
    if filename != "":
        if filename.startswith(directory):
            logging.info("delete " + filename)
            try:
                if os.path.isfile(filename):
                    os.remove(filename)
                    # if ovpn file is deleted, remove it from dialog
                    ovpnfilename = self.vpnInputovpn.text()
                    if filename == ovpnfilename:
                        self.vpnInputovpn.setText("")
                    
            except OSError as error:
                logging.error(error)
                common.errorDialog(error)
        else:
            logging.info("no delete " + filename)
            common.errorDialog(common.getRessource("systemErrorDeleteFile"))
    
    
def readVPN(self):
    logging.info("readVPN")
    values = {}
    vpnfile = common.getRessource("VPNFile")
    if os.path.isfile(vpnfile):
        try:
            filer = open(vpnfile, "r")
            for line in filer:
                line = line.strip()
                name = line.split("=", 2)
                values[name[0]] = name[1]
            filer.close()
        except IOError as error:
            logging.error(error)
            common.errorDialog(error)
    return values


def writeVPN(values):
    logging.info("writeVPN")
    try:
        tmpfile = common.getRessource("tmpFile")
        filew = open(tmpfile, "w")
        if values["ovpn"] != "":
            line = "ovpn=" + values["ovpn"] + "\n"
            filew.write(line)
        if values["parametervpn"] != "":
            line = "parametervpn=" + values["parametervpn"] + "\n"
            filew.write(line)
        line = "autostartvpn=" + values["autostartvpn"] + "\n"
        filew.write(line)
        line = "systemlogin=" + values["systemlogin"] + "\n"
        filew.write(line)
        filew.close()
    except OSError as error:
        logging.error(error)
        common.errorDialog(error)
    try:
        # write file to system
        command = common.getRessource("commandVPNFile")
        command = command + " " + tmpfile
        common.runProgram(command)
    except OSError as error:
        logging.error(error)
        common.errorDialog(error)
        
        
def getFile(parameter, directory):
    dialog = QtWidgets.QFileDialog()
    dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)    
    if parameter == "ovpn":
        dialog.setNameFilters(["OVPN files (*.ovpn)"])
    dialog.setDirectory(directory)
    filename = ""
    if dialog.exec_():
        filenames = dialog.selectedFiles()
        filename = filenames[0]
    return filename

