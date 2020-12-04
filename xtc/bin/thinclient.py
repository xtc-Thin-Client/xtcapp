#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-

# File:    thinclient.py
# Author:  Volker Matheis
#
# Release: 1.6
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
import common
import connectThread
import dialoglogin
import dialogpassword
import dialogrdesktop
import dialogrdp
import dialogrealvnc
import dialogssh
import dialogtigervnc
import dialogtightvnc
import dialogx2go
import dialogxdmcp
import logging
import os
import sys
import thinclientui
import time
import vpn


class thinClientUI(QtWidgets.QMainWindow, thinclientui.Ui_MainWindow):
    connectedThreads = {}

    def __init__(self, configfile):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.configfile = configfile
        if self.configfile == "":
            self.configfile = "thinclient.conf"
        if not os.path.isfile(self.configfile):
            print("ERROR: Config file not found: " + self.configfile)
            sys.exit(1)

        # logging
        loggingfilename = common.getRessourceByName(self.configfile, "loggingFile")
        debugfile = common.getRessourceByName(self.configfile, "debugSwitch")
        debug = False
        if os.path.isfile(debugfile):
            debug = True
        common.loggingStart(loggingfilename, debug)
        # init system
        common.getSystemFile(self.configfile)
        common.setRessourceFile(self.configfile)
        systemLanguage = common.getLanguage()
        # delete existing config file
        common.deleteConfigScript()
        
        # label
        self.connectButton.setText(common.getRessource("connect"))
        self.connectButtonCancel.setText(common.getRessource(
                                         "connectButtonCancel"))
        self.connectButtonExtended.setText(common.getRessource(
                                           "connectButtonExtended"))
        self.systemButtonReboot.setText(common.getRessource(
                                        "systemButtonReboot"))
        self.systemButtonShutdown.setText(common.getRessource(
                                          "systemButtonShutdown"))
        self.configButtonNew.setText(common.getRessource(
                                     "configButtonNew"))
        self.configButtonEdit.setText(common.getRessource(
                                      "configButtonEdit"))
        self.configButtonDelete.setText(common.getRessource(
                                        "configButtonDelete"))
        self.networkLabelInterface.setText(common.getRessource(
                                           "networkLabelInterface"))                                        
        self.networkInputDHCP.setText(common.getRessource("networkInputDHCP"))
        self.networkInputStaticIP.setText(common.getRessource(
                                          "networkInputStaticIP"))
        self.networkLabelAddress.setText(common.getRessource(
                                         "networkLabelAddress"))
        self.networkLabelSubnetmask.setText(common.getRessource(
                                            "networkLabelSubnetmask"))
        self.networkLabelGateway.setText(common.getRessource(
                                         "networkLabelGateway"))
        self.networkLabelDNS.setText(common.getRessource("networkLabelDNS"))
        self.networkLabelWlanSSID.setText(common.getRessource("networkLabelWlanSSID"))
        self.networkLabelWlanPassword.setText(common.getRessource("networkLabelWlanPassword"))
        self.networkButtonTransfer.setText(common.getRessource(
                                           "networkButtonTransfer"))
        self.systemButtonTerminal.setText(common.getRessource(
                                          "systemButtonTerminal"))
        self.systemLabelLanguage.setText(common.getRessource(
                                         "systemLabelLanguage"))
        self.systemLabelKeyboardLayout.setText(common.getRessource(
                                               "systemLabelKeyboardLayout"))
        self.systemInputStartAdmin.setText(common.getRessource(
                                           "systemStartAdmin"))
        self.systemLabelPassword.setText(common.getRessource(
                                         "systemLabelPassword"))
        self.systemLabelPasswordRepeat.setText(common.getRessource(
                                               "systemLabelPasswordRepeat"))
        self.systemInputRemoteVNC.setText(common.getRessource(
                                          "systemInputRemoteVNC"))
        self.systemLabelRemotePassword.setText(common.getRessource(
                                               "systemLabelRemotePassword"))
        self.systemLabelRemotePasswordRepeat.setText(common.getRessource(
                                                     "systemLabelRemotePasswordRepeat"))                                               
        self.systemInputSSH.setText(common.getRessource(
                                    "systemInputSSH"))                                               
        self.systemInputUSBAutomount.setText(common.getRessource(
                                    "systemInputUSBAutomount"))                                                       
        self.systemInputOneninedesign.setText(common.getRessource(
                                    "systemInputOneninedesign"))                                               
        self.systemInputArgon1.setText(common.getRessource(
                                    "systemInputArgon1"))                                                       
        self.systemButtonAssume.setText(common.getRessource(
                                        "systemButtonAssume"))
        self.systemInputScreensaver.setText(common.getRessource(
                                            "systemScreensaver"))
        self.systemInputMonitorStandby.setText(common.getRessource(
                                               "systemMonitorStandby"))
        self.systemLabelResolution.setText(common.getRessource(
                                           "systemLabelResolution"))
        #self.systemMonitorGroupBox.setTitle(common.getRessource(
        #                                  "systemMonitorGroupBox"))                                               
        self.vpnLabelovpn.setText(common.getRessource(
                                  "vpnLabelovpn"))
        self.vpnInputSystemLogin.setText(common.getRessource(
                                         "configDialogLabelSystemLogin"))
        self.vpnInputAutostart.setText(common.getRessource(
                                       "configDialogLabelAutostart"))                                
        self.vpnButtonConnect.setText(common.getRessource(
                                      "vpnButtonConnect"))                                
        self.vpnButtonCancel.setText(common.getRessource(
                                     "vpnButtonCancel"))
        self.vpnLabelParameter.setText(common.getRessource(
                                       "configDialogLabelParameter"))                                
        self.vpnButtonTransfer.setText(common.getRessource(
                                       "networkButtonTransfer"))
        self.vpnButtonCondition.setText(common.getRessource(
                                        "vpnButtonCondition"))
        self.vpnButtonCondition.setIcon(QtGui.QIcon(common.getRessource("disconnectIcon")))
        self.vpnButtonFiles.setText(common.getRessource(
                                    "vpnButtonAdditionalFiles"))
        
        pixmap = QPixmap(common.getRessource("connectIcon"))
        self.systemLabelInfoImage.setPixmap(pixmap)
        self.thinClientTab.setTabText(0, common.getRessource("tabConnect"))
        self.thinClientTab.setTabText(1, common.getRessource("tabSystem"))
        self.thinClientTab.setTabText(2, common.getRessource("tabConfig"))
        self.thinClientTab.setTabText(3, common.getRessource("tabNetwork"))
        self.thinClientTab.setTabText(4, common.getRessource("tabVPN"))
        self.thinClientTab.setTabText(5, common.getRessource("tabSystem"))

        # widget actions
        self.connectButton.clicked.connect(self.connection)
        self.connectButtonCancel.clicked.connect(self.connectionCancel)
        self.connectButtonExtended.clicked.connect(self.connectionExtended)
        self.configButtonNew.clicked.connect(self.configNewConnection)
        self.configButtonEdit.clicked.connect(self.configEdit)
        self.configButtonDelete.clicked.connect(self.configDelete)
        self.networkInputDHCP.toggled.connect(self.networkType)
        self.networkInputStaticIP.toggled.connect(self.networkType)
        self.networkButtonTransfer.clicked.connect(self.networkTransfer)
        self.systemButtonReboot.clicked.connect(self.systemReboot)
        self.systemButtonShutdown.clicked.connect(self.systemShutdown)
        self.connectList.doubleClicked.connect(self.connection)
        self.configList.doubleClicked.connect(self.configListItem)
        self.systemButtonTerminal.clicked.connect(self.systemTerminal)
        self.systemButtonAssume.clicked.connect(self.systemAssume)                
        self.vpnButtonFile.clicked.connect(self.vpnGetFile)
        self.vpnButtonTransfer.clicked.connect(self.vpnTransfer)
        self.vpnButtonConnect.clicked.connect(self.vpnConnect)
        self.vpnButtonCancel.clicked.connect(self.vpnCancel)
        self.vpnButtonCondition.clicked.connect(self.vpnCondition)
        self.vpnButtonFiles.clicked.connect(self.vpnAdditionalFiles)
        self.systemInputArgon1.toggled.connect(self.systemCaseArgon1)
        self.systemInputOneninedesign.toggled.connect(self.systemCaseOneninedesign)
        
        # get system
        #system = common.runProgramResult(common.getRessource("commandGetSystem"))
        system = common.getSystem()
        if system != "PI4":
            self.systemInputArgon1.setEnabled(False)
            self.systemInputOneninedesign.setEnabled(False)
            
        # read network        
        interfaces = common.readConnectionInterfaces()
        for interface in interfaces:
            self.networkInputInterface.addItem(interface)
            
        for interface in interfaces:
            if common.isNetworkInterfaceUp(interface):
                index = self.networkInputInterface.findText(interface,
                                                            QtCore.Qt.MatchFixedString)
                self.networkInputInterface.setCurrentIndex(index)
            
        values = common.readNetwork(self)
        dhcp = True
        if "dhcp" in values:
            dhcp = values["dhcp"]
        if "address" in values:
            self.networkInputAddress.setText(values["address"])
        if "netmask" in values:
            self.networkInputSubnetmask.setText(values["netmask"])
        if "gateway" in values:
            self.networkInputGateway.setText(values["gateway"])
        if "dns" in values:
            self.networkInputDNS.setText(values["dns"])
        if "ssid" in values:
            self.networkInputWlanSSID.setText(values["ssid"])
        if "password" in values:
            self.networkInputWlanPassword.setText(values["password"])
        
        if dhcp:
            self.networkInputDHCP.setChecked(True)
            self.networkInputStaticIP.setChecked(False)
        else:
            self.networkInputDHCP.setChecked(False)
            self.networkInputStaticIP.setChecked(True)

        # fill ComboBox with connection types
        common.fillComboBox(self, "configConnectionType",
                            self.configInputConnectionType)
        # Get Language
        common.fillComboBox(self, "language", self.systemInputLanguage)
        if systemLanguage == "DE":
            language = "Deutsch"
            index = self.systemInputLanguage.findText(language,
                                                      QtCore.Qt.MatchFixedString)
            self.systemInputLanguage.setCurrentIndex(index)

        # Get Keyboard Layout
        values = common.getKeyboardLayouts()
        common.fillComboBoxList(self, values, self.systemInputKeyboardLayout)
        layout = common.getCurrentKeyboardLayout()
        index = self.systemInputKeyboardLayout.findText(layout,
                                                        QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.systemInputKeyboardLayout.setCurrentIndex(index)

        # Check VNC
        if common.isRemoteVNC():
            self.systemInputRemoteVNC.setChecked(True)
        # Check SSH
        if common.isRemoteSSH():
            self.systemInputSSH.setChecked(True)
        # check USB automount
        if common.isUSBAutomount():
            self.systemInputUSBAutomount.setChecked(True)
            
        # hide tabs when in user mode
        startadmin = True
        autostartvpn = False
        values = common.readSystem()
        if "startAdmin" in values:
            if values["startAdmin"] == "yes":
                self.systemInputStartAdmin.setChecked(True)
            if values["startAdmin"] == "no":
                startadmin = False
        if not "adminPassword" in values:
            startadmin = True
        if "adminPassword" in values:
            if values["adminPassword"] == "":
                startadmin = True
        values = vpn.readVPN(self)
        if "ovpn" in values:
            self.vpnInputovpn.setText(values["ovpn"])
        if "parametervpn" in values:
            self.vpnInputParameter.setText(values["parametervpn"])
        if "systemlogin" in values:
            if values["systemlogin"] == "yes":
                self.vpnInputSystemLogin.setChecked(True)                
        if "autostartvpn" in values:
            if values["autostartvpn"] == "yes":
                self.vpnInputAutostart.setChecked(True)
                autostartvpn = True                            
        if startadmin is True:
            self.connectButtonExtended.setEnabled(False)
        else:
            common.enableTabs(self, False)        
        # get screensaver state
        if common.isScreensaver():
            self.systemInputScreensaver.setChecked(True)
        else:
            self.systemInputScreensaver.setChecked(False)
            
        # get monitor standby state
        if common.isMonitorStandby():
            self.systemInputMonitorStandby.setChecked(True)
        else:
            self.systemInputMonitorStandby.setChecked(False)
            
        # get state Oneninedesign power case
        if common.isOneninedesign():
            self.systemInputOneninedesign.setChecked(True)
        else:
            self.systemInputOneninedesign.setChecked(False)
            
        # get state Argop1 power case
        if common.isArgon1():
            self.systemInputArgon1.setChecked(True)
        else:
            self.systemInputArgon1.setChecked(False)        
            
        # set title
        self.setWindowTitle(common.getRessource("dialogTitle"))
        # Select first Tab
        self.thinClientTab.setCurrentIndex(0)
        # start vpn connection
        if autostartvpn:
            parameter = None
            systemlogin = None
            if "parametervpn" in values:
                parameter = values["paramtervpn"]
            systemlogin = None
            if "systemlogin" in values:
                systemlogin = values["systemlogin"]
            vpn.autostartvpn(self, values["ovpn"], parameter, systemlogin)
        # autostart connections
        self.autostart()
        # read existing connections
        self.fillListWidgets()
        # get resolution
        resolution = common.getResolution()
        self.systemInputResolution.setText(resolution)

    def closeEvent(self, event):
        logging.info("close")
        common.systemShutdown(self)
        #event.ignore()

    def fillListWidgets(self):
        common.fillListWidgets(self, self.connectedThreads)

# Connection
    def connectionExtended(self):
        logging.info("connectionExtended")
        dialogPassword = dialogpassword.dialogPasswordUI(self.configfile)
        dialogPassword.exec_()
        result = dialogPassword.getResult()
        if result is True:
            password = dialogPassword.getPassword()
            values = common.readSystem()
            if "adminPassword" in values:
                inputpassword = common.convertPassword(password)
                if values["adminPassword"] == inputpassword:
                    common.enableTabs(self, True)
                else:
                    common.messageDialog("connectExtendedPasswordError")
            else:
                common.enableTabs(self, True)

        
    def autostart(self):
        logging.info("autostart")
        connections = common.readAllConnections()
        for index in range(len(connections)):
            name = connections[index]
            values = common.readConnection(name)
            if values["autostart"] == "yes":
                self.connectionExec(values)

    def connection(self):
        logging.info("connection")
        item = self.connectList.currentItem()
        if item is not None:
            name = item.text()
            if not name in self.connectedThreads:
                values = common.readConnection(name)
                self.connectionExec(values)
                self.fillListWidgets()

        
    def connectionExec(self, values):
        logging.info("connectionExec")
        
        repeat = True
        while repeat:
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
                    dialogLogin = dialoglogin.dialogLoginUI(self.configfile, connectionname)
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
                runconnect = connectThread.connectThread(command, connectionname)
                runconnect.threadCancel.connect(self.connectThreadCancel)
                #self.connect(runconnect, QtCore.SIGNAL(
                #             "connectThreadCancel(QString)"), self.connectThreadCancel)
                self.connectedThreads[connectionname] = runconnect
                runconnect.start()
                break
            else:
                #common.messageDialog("connectNoConnection", False)
                repeat = common.cancelDialog("connectNoConnection")            

# called by Button "Cancel connection"
    def connectionCancel(self):
        logging.info("connectionCancel")
        item = self.connectList.currentItem()
        if item is not None:
            name = item.text()
            if name in self.connectedThreads:
                runconnect = self.connectedThreads[name]
                if runconnect is not None:
                    pid = runconnect.getPid()
                    command = common.getRessource("commandKill")
                    command = command + " " + str(pid)
                    common.runProgram(command)

# called by threadConnect when connection end
    def connectThreadCancel(self, name):
        logging.info(name)
        runconnect = self.connectedThreads[name]
        runconnect.terminate()
        # show connection list
        del self.connectedThreads[name]        
        time.sleep(1)
        # repeat connection
        self.repeatConnection(name)
        self.fillListWidgets()

# repeat a cancelled connection
    def repeatConnection(self, name):
        result = common.isRepeat(name)
        logging.info(result)
        if result is True:
            values = common.readConnection(name)
            self.connectionExec(values)

# Configuration
    def configListItem(self):
        logging.info("configList")
        self.configEdit()

    def configNewConnection(self):
        logging.info("newConnection")
        connectiontype = self.configInputConnectionType.currentText()
        if connectiontype == "VNC":
            self.configNewConnectionVNC()
        elif connectiontype == "RDP (xfreerdp)":
            self.configNewConnectionRDP()
        elif connectiontype == "RDP (rdesktop)":
            self.configNewConnectionRDesktop()
        elif connectiontype == "XDMCP":
            self.configNewConnectionxdmcp()
        elif connectiontype == "X2Go":
            self.configNewConnectionx2go()
        elif connectiontype == "ssh":
            self.configNewConnectionssh()

    def configNewConnectionVNC(self):
        logging.info("newConnectionVNC")
        viewer = common.getVNCViewer()
        if viewer == "tigervnc":
            dialogConnection = dialogtigervnc.dialogTigerVNCUI("", self.configfile)
        if viewer == "tightvnc":
            dialogConnection = dialogtightvnc.dialogTightVNCUI("", self.configfile)
        if viewer == "realvnc":
            dialogConnection = dialogrealvnc.dialogRealVNCUI("", self.configfile)
        dialogConnection.exec_()
        self.fillListWidgets()

    def configNewConnectionRDP(self):
        logging.info("newConnectionRDP")
        dialogConnection = dialogrdp.dialogRDPUI("", self.configfile)
        dialogConnection.exec_()
        self.fillListWidgets()
        
    def configNewConnectionRDesktop(self):
        logging.info("newConnectionRDesktop")
        dialogConnection = dialogrdesktop.dialogRDesktopUI("", self.configfile)
        dialogConnection.exec_()
        self.fillListWidgets()

    def configNewConnectionssh(self):
        logging.info("newConnectionssh")
        dialogConnection = dialogssh.dialogsshUI("", self.configfile)
        dialogConnection.exec_()
        self.fillListWidgets()

    def configNewConnectionxdmcp(self):
        logging.info("newConnectionxdmcp")
        dialogConnection = dialogxdmcp.dialogxdmcpUI("", self.configfile)
        dialogConnection.exec_()
        self.fillListWidgets()

    def configNewConnectionx2go(self):
        logging.info("newConnectionx2go")
        dialogConnection = dialogx2go.dialogx2goUI("", self.configfile)
        dialogConnection.exec_()
        self.fillListWidgets()

    def configEdit(self):
        logging.info("configEdit")
        item = self.configList.currentItem()
        if item is not None:
            name = item.text()
            connection = common.readConnection(name)
            if connection["typ"] == "vnc":
                viewer = common.getVNCViewer()
                if viewer == "tigervnc":
                    dialogConnection = dialogtigervnc.dialogTigerVNCUI(name, self.configfile)
                if viewer == "tightvnc":
                    dialogConnection = dialogtightvnc.dialogTightVNCUI(name, self.configfile)
                if viewer == "realvnc":
                    dialogConnection = dialogrealvnc.dialogRealVNCUI(name, self.configfile)
                dialogConnection.exec_()
            if connection["typ"] == "ssh":
                dialogConnection = dialogssh.dialogsshUI(name, self.configfile)
                dialogConnection.exec_()
            if connection["typ"] == "xdmcp":
                dialogConnection = dialogxdmcp.dialogxdmcpUI(name, self.configfile)
                dialogConnection.exec_()
            if connection["typ"] == "x2go":
                dialogConnection = dialogx2go.dialogx2goUI(name, self.configfile)
                dialogConnection.exec_()
            if connection["typ"] == "rdp":
                dialogConnection = dialogrdp.dialogRDPUI(name, self.configfile)
                dialogConnection.exec_()
            if connection["typ"] == "rdesktop":
                dialogConnection = dialogrdesktop.dialogRDesktopUI(name, self.configfile)
                dialogConnection.exec_()
        self.fillListWidgets()

    def configDelete(self):
        logging.info("configDelete")
        item = self.configList.currentItem()
        if item is not None:
            result = common.confirmDialog(self,
                                          common.getRessource("configDeleteDialogTitle"),
                                          common.getRessource("configDeleteDialogMessage"))
            if result:
                common.deleteConnection(item.text())
                self.fillListWidgets()

# Network
    def networkType(self):
        if self.networkInputDHCP.isChecked():
            self.networkInputAddress.setEnabled(False)
            self.networkInputGateway.setEnabled(False)
            self.networkInputDNS.setEnabled(False)
            self.networkInputSubnetmask.setEnabled(False)
            logging.info("networkDHCP")
        else:
            self.networkInputStaticIP.setChecked(True)
            self.networkInputAddress.setEnabled(True)
            self.networkInputGateway.setEnabled(True)
            self.networkInputDNS.setEnabled(True)
            self.networkInputSubnetmask.setEnabled(True)
            logging.info("networkStaticIP")

    def networkTransfer(self):
        logging.info("networkTransfer")
        if self.networkInputDHCP.isChecked():
            common.networkWriteDHCP(self)
        else:
            common.networkWriteStaticIP(self)
    
# System
    def systemTerminal(self):
        logging.info("systemTerminal")
        common.systemTerminal()

    def systemCaseArgon1(self):
        logging.info("systemCaseTypeArgon1")
        if self.systemInputArgon1.isChecked():
            self.systemInputOneninedesign.setChecked(False)
            
    def systemCaseOneninedesign(self):
        logging.info("systemCaseTypeOneninedesign")    
        if self.systemInputOneninedesign.isChecked():
            self.systemInputArgon1.setChecked(False)        
        
    def systemAssume(self):
        logging.info("systemAssume")
        values = {}
        password = self.systemInputPassword.text()
        passwordrepeat = self.systemInputPasswordRepeat.text()
        if password != "" or passwordrepeat != "":
            if password == passwordrepeat:
                values["adminPassword"] = common.convertPassword(password)
            else:
                common.messageDialog("systemPasswordComparisonError")
                return

        if self.systemInputStartAdmin.isChecked():
            values["startAdmin"] = "yes"
        else:
            values["startAdmin"] = "no"

        if self.systemInputRemoteVNC.isChecked():
            password = self.systemInputRemotePassword.text()
            passwordrepeat = self.systemInputRemotePasswordRepeat.text()

            if password == "" or passwordrepeat == "":
                common.messageDialog("systemRemotePasswordError")
                return             
            
            if password == passwordrepeat:
                common.remoteVNC(True, self)
            else:
                common.messageDialog("systemPasswordComparisonError")                
                return
        else:
            common.remoteVNC(False, self)
            
        if self.systemInputSSH.isChecked():
            common.remoteSSH(True)
        else:
            common.remoteSSH(False)
                    
        values["language"] = self.systemInputLanguage.currentText()
        values["keyboardLayout"] = self.systemInputKeyboardLayout.currentText()
        common.writeSystem(values)
        common.writeKeyboardLayout(values["keyboardLayout"])
        # reboot system
        result = common.confirmDialog(self,
                                      common.getRessource("systemShutdownTitle"),
                                      common.getRessource("systemAssumeMessage"))
                                      
        common.deleteConfigScript()
        if self.systemInputScreensaver.isChecked():
            common.setScreensaver("on")
        else:
            common.setScreensaver("off")
        if self.systemInputMonitorStandby.isChecked():
            common.setMonitorStandby("on")
        else:
            common.setMonitorStandby("off")
            
        if result:       
            common.deleteConfigScript()
            if self.systemInputScreensaver.isChecked():
                common.setScreensaver("on")
            else:
                common.setScreensaver("off")
                
            if self.systemInputMonitorStandby.isChecked():
                common.setMonitorStandby("on")
            else:
                common.setMonitorStandby("off")
            common.setResolution(self.systemInputResolution.text())
            
            if self.systemInputUSBAutomount.isChecked():
                common.setUSBAutomount("on")
            else:
                common.setUSBAutomount("off")
                
            common.setResolution(self.systemInputResolution.text())            
            if self.systemInputOneninedesign.isChecked():
                common.setOneninedesign("on")
            else:
                common.setOneninedesign("off")
                
            if self.systemInputArgon1.isChecked():
                common.setArgon1("on")
            else:
                common.setArgon1("off")            

            common.runProgram(common.getRessource("commandReboot"))

    def systemReboot(self):
        common.systemReboot(self)

    def systemShutdown(self):
        common.systemShutdown(self)
        
# vpn
    def vpnGetFile(self):
        logging.info("vpnGetFile")
        vpn.vpnGetFile(self)
        
    def vpnTransfer(self):
        logging.info("vpnTransfer")
        vpn.vpnTransfer(self)        
        # reboot system
        result = common.confirmDialog(self,
                                      common.getRessource("systemShutdownTitle"),
                                      common.getRessource("systemAssumeMessage"))
        if result:
            common.runProgram(common.getRessource("commandReboot"))
        
    def vpnConnect(self):
        logging.info("vpnConnection")
        vpn.vpnConnect(self)
            
    def vpnCancel(self):
        logging.info("vpnCancel")
        vpn.vpnCancel(self)
            
    def vpnCondition(self): 
        logging.info("vpnCondition")
        vpn.vpnCondition(self)
        
    def vpnAdditionalFiles(self): 
        logging.info("vpnAdditionalFiles")
        vpn.vpnAdditionalFiles(self)
        
        
def main():
    configfile = ""
    if len(sys.argv) > 1:
        args = sys.argv
        configfile = args[1]

    app = QtWidgets.QApplication(sys.argv)
    form = thinClientUI(configfile)
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
