#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-

# File:    thinclient.py
# Author:  Volker Matheis
#
# Release: 1.8
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
import logging
import os
import sys
import time
from datetime import datetime, timedelta
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
import thinclientui
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
        loggingfilename = common.getRessourceByName(self.configfile, "loggingFileThinclient")
        debugfile = common.getRessourceByName(self.configfile, "debugSwitch")
        debug = False
        if os.path.isfile(debugfile):
            debug = True
        common.loggingStart(loggingfilename, debug)
        # init system
        common.getSystemFile(self.configfile)
        common.setRessourceFile(self.configfile)
        systemLanguage = common.getLanguage()
        # delete connection log file
        common.deleteConnectionLog()
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
        self.connectButtonLog.setText(common.getRessource(
                                          "connectButtonLog"))
        self.configButtonNew.setText(common.getRessource(
                                     "configButtonNew"))
        self.configButtonEdit.setText(common.getRessource(
                                      "configButtonEdit"))
        self.configButtonDelete.setText(common.getRessource(
                                        "configButtonDelete"))
        self.networkInputSave.setText(common.getRessource(
                                           "networkInputSave"))
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
        self.networkInputSearchSSID.setText(common.getRessource("networkInputSearchSSID"))
        self.networkLabelWlanPassword.setText(common.getRessource("networkLabelWlanPassword"))
        self.systemButtonTerminal.setText(common.getRessource(
                                          "systemButtonTerminal"))
        self.systemInputMinimize.setText(common.getRessource(
                                         "systemInputMinimize"))
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
        self.systemLabelsshPassword.setText(common.getRessource(
                                         "systemLabelsshPassword"))
        self.systemLabelsshPasswordRepeat.setText(common.getRessource(
                                         "systemLabelsshPasswordRepeat"))        
        self.systemInputUSBAutomount.setText(common.getRessource(
                                    "systemInputUSBAutomount"))                                                       
        self.systemInputOneninedesign.setText(common.getRessource(
                                    "systemInputOneninedesign"))                                               
        self.systemInputArgon1.setText(common.getRessource(
                                    "systemInputArgon1"))                                                       
        self.systemInputScreensaver.setText(common.getRessource(
                                            "systemScreensaver"))
        self.systemInputMonitorStandby.setText(common.getRessource(
                                               "systemMonitorStandby"))
        self.systemLabelResolution.setText(common.getRessource(
                                           "systemLabelResolution"))
        self.systemLabelResolution2.setText(common.getRessource(
                                           "systemLabelResolution2"))
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
        self.vpnButtonCondition.setText(common.getRessource(
                                        "vpnButtonCondition"))
        self.vpnButtonCondition.setIcon(QtGui.QIcon(common.getRessource("disconnectIcon")))
        self.vpnButtonFiles.setText(common.getRessource(
                                    "vpnButtonAdditionalFiles"))
        self.vpnButtonDelete.setText(common.getRessource(
                                    "vpnButtonDelete"))
        self.saveButtonSave.setText(common.getRessource(
                                    "saveButtonSave"))
        self.systemLabelSound.setText(common.getRessource(
                                    "systemLabelSound"))
        self.systemInputMultiMonitorLeft.setText(common.getRessource(
                                    "systemInputMultiMonitorLeft"))
        self.systemInputMultiMonitorRight.setText(common.getRessource(
                                    "systemInputMultiMonitorRight"))
        self.systemInputMultiMonitorAbove.setText(common.getRessource(
                                    "systemInputMultiMonitorAbove"))
        self.systemInputMultiMonitorBelow.setText(common.getRessource(
                                    "systemInputMultiMonitorBelow"))
        self.timeInputSave.setText(common.getRessource(
                                    "timeInputSave"))
        self.timeInputAuto.setText(common.getRessource(
                                    "timeInputAuto"))
        self.timeInputView.setText(common.getRessource(
                                    "timeInputView"))
        self.timeLabelTime.setText(common.getRessource(
                                    "timeLabelTime"))
        self.timeLabelNTP.setText(common.getRessource(
                                    "timeLabelNTP"))
        self.timeLabelActionGroup.setTitle(common.getRessource(
                                    "timeLabelActionGroup"))
        self.timeInputAction.setText(common.getRessource(
                                    "timeInputAction"))
        self.timeLabelActionAction.setText(common.getRessource(
                                    "timeLabelActionAction"))
        self.timeLabelActionTime.setText(common.getRessource(
                                    "timeLabelActionTime"))
        self.timeInputActionRepeat.setText(common.getRessource(
                                    "timeInputActionRepeat"))
        self.timeLabelActionLast.setText(common.getRessource(
                                    "timeLabelActionLast"))
        self.timeLabelTimezone.setText(common.getRessource(
                                    "timeLabelTimezone"))

        self.timeInputTime.setDisplayFormat("yyyy-MM-dd HH:mm") 
        # get current time and show
        self.timeInputTime.setDateTime(QtCore.QDateTime.currentDateTime())
        
        pixmap = QPixmap(common.getRessource("connectIcon"))
        self.systemLabelInfoImage.setPixmap(pixmap)
        self.thinClientTab.setTabText(0, common.getRessource("tabConnect"))
        self.thinClientTab.setTabText(1, common.getRessource("tabSystem"))
        self.thinClientTab.setTabText(2, common.getRessource("tabConfig"))
        self.thinClientTab.setTabText(3, common.getRessource("tabNetwork"))
        self.thinClientTab.setTabText(4, common.getRessource("tabVPN"))
        self.thinClientTab.setTabText(5, common.getRessource("tabSystem"))
        self.thinClientTab.setTabText(6, common.getRessource("tabHardware"))
        self.thinClientTab.setTabText(7, common.getRessource("tabMonitor"))
        self.thinClientTab.setTabText(8, common.getRessource("tabTime"))
        self.thinClientTab.setTabText(9, common.getRessource("tabSave"))

        # widget actions
        self.connectButton.clicked.connect(self.connection)
        self.connectButtonCancel.clicked.connect(self.connectionCancel)
        self.connectButtonExtended.clicked.connect(self.connectionExtended)
        self.configButtonNew.clicked.connect(self.configNewConnection)
        self.configButtonEdit.clicked.connect(self.configEdit)
        self.configButtonDelete.clicked.connect(self.configDelete)
        self.networkInputDHCP.toggled.connect(self.networkType)
        self.networkInputStaticIP.toggled.connect(self.networkType)
        self.systemButtonReboot.clicked.connect(self.systemReboot)
        self.systemButtonShutdown.clicked.connect(self.systemShutdown)
        self.connectButtonLog.clicked.connect(self.connectionLog)
        self.connectList.doubleClicked.connect(self.connection)
        self.configList.doubleClicked.connect(self.configListItem)
        self.systemButtonTerminal.clicked.connect(self.systemTerminal)
        self.vpnButtonFile.clicked.connect(self.vpnGetFile)
        self.vpnButtonDelete.clicked.connect(self.vpnDeleteFile)
        self.vpnButtonConnect.clicked.connect(self.vpnConnect)
        self.vpnButtonCancel.clicked.connect(self.vpnCancel)
        self.vpnButtonCondition.clicked.connect(self.vpnCondition)
        self.vpnButtonFiles.clicked.connect(self.vpnAdditionalFiles)
        self.systemInputArgon1.toggled.connect(self.systemCaseArgon1)
        self.systemInputOneninedesign.toggled.connect(self.systemCaseOneninedesign)
        self.saveButtonSave.clicked.connect(self.save)
        self.systemInputRemotePassword.textChanged.connect(self.remotePasswordChanged)
        self.systemInputPassword.textChanged.connect(self.passwordChanged)
        self.systemInputsshPassword.textChanged.connect(self.sshPasswordChanged)
        self.networkInputSearchSSID.clicked.connect(self.searchSSID)

        # read network        
        interfaces = common.readConnectionInterfaces()
        for interface in interfaces:
            self.networkInputInterface.addItem(interface)
            
        for interface in interfaces:
            if common.isNetworkInterfaceUp(interface):
                index = self.networkInputInterface.findText(interface,
                                                            QtCore.Qt.MatchFixedString)
                self.networkInputInterface.setCurrentIndex(index)
            
        # get wlan devices
        self.searchSSID()
            
        values = common.readNetwork(self)
        if len(values) == 0:
            self.networkInputSave.setChecked(True)
            
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
            index = self.networkInputWlanSSID.findText(values["ssid"], QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.networkInputWlanSSID.setCurrentIndex(index)
            else:
                if values["ssid"] != "":
                    self.networkInputWlanSSID.addItem(values["ssid"])
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

        # Get Resolution List
        resolution, resolution2 = common.getResolutionList()
        common.fillComboBoxList(self, resolution, self.systemInputResolution)
        common.fillComboBoxList(self, resolution2, self.systemInputResolution2)
        
        # get orientation 
        orientation = common.getOrientationMonitor2()
        if orientation == "left":
            self.systemInputMultiMonitorLeft.setChecked(True)
        if orientation == "right":
            self.systemInputMultiMonitorRight.setChecked(True)
        if orientation == "above":
            self.systemInputMultiMonitorAbove.setChecked(True)
        if orientation == "below":
            self.systemInputMultiMonitorBelow.setChecked(True)

        # Check VNC
        if common.isRemoteVNC():
            self.systemInputRemoteVNC.setChecked(True)
        # Check SSH
        if common.isRemoteSSH():
            self.systemInputSSH.setChecked(True)
            self.systemInputsshPassword.setText("1111111111")
        # check USB automount
        if common.isUSBAutomount():
            self.systemInputUSBAutomount.setChecked(True)

        # set time parameter
        if common.isDateShow():
            self.timeInputView.setChecked(True)
        # list time zones
        values = common.getTimezones()
        common.fillComboBoxList(self, values, self.timeInputTimezone)
        # fill action
        common.fillComboBox(self, "timeActions", self.timeInputActionAction)
        
        # is date and time showing?
        value = common.isDateShow()
        if value:
            self.timeInputView.setChecked(True)
            
        # get time parameter
        timeValues = common.readTime()
        for value in timeValues:
            if "save" in value:
                if timeValues["save"] == "no":
                    self.timeInputSave.setChecked(True)
            if "automatic" in value:
                if timeValues["automatic"] == "yes":
                    self.timeInputAuto.setChecked(True)
            if "ntp" in value:
                self.timeInputNTP.setText(timeValues["ntp"])
            if "zone" in value:
                index = self.timeInputTimezone.findText(timeValues["zone"], QtCore.Qt.MatchFixedString)
                if index < 0:
                    index = 0
                self.timeInputTimezone.setCurrentIndex(index)
            if "time" in value:
                time = datetime.strptime(timeValues["time"], "%Y-%m-%d %H:%M")
                self.timeInputTime.setDateTime(time)
            if "execute" in value:
                if timeValues["execute"] == "yes":
                    self.timeInputAction.setChecked(True)
            if "repeat" in value:
                if timeValues["repeat"] == "yes":
                    self.timeInputActionRepeat.setChecked(True)
            if "action" in value:
                index = self.timeInputActionAction.findText(timeValues["action"], QtCore.Qt.MatchFixedString)
                self.timeInputActionAction.setCurrentIndex(index)
            if "execat" in value:
                if timeValues["execat"].startswith("+"):
                    self.timeInputActionTime.setText(timeValues["execat"])
                else:
                    if timeValues["execat"] != "":
                        time = datetime.strptime(timeValues["execat"], "%Y-%m-%d %H:%M")
                        strtime = time.strftime("%Y-%m-%d %H:%M")
                        self.timeInputActionTime.setText(strtime)
            if "last" in value:
                self.timeInputActionLast.setText(timeValues["last"])
        
        # hide tabs when in user mode
        startadmin = True
        autostartvpn = False
        values = common.readSystem()
        self.systemInputStartAdmin.setChecked(True)
        if "startAdmin" in values:
            if values["startAdmin"] == "no":
                startadmin = False
                self.systemInputStartAdmin.setChecked(False)
        if not "adminPassword" in values:
            startadmin = True
        if "adminPassword" in values:
            self.systemInputPassword.setText(values["adminPassword"])
            if values["adminPassword"] == "":
                startadmin = True
        # minimize dialog?
        if "startMinimized" in values:
            if values["startMinimized"] == "yes":
                self.systemInputMinimize.setChecked(True)
                self.showMinimized()
        # save network
        if "networkSave" in values:
            if values["networkSave"] == "no":
                self.networkInputSave.setChecked(True)
                
        # get current resolution
        resolution, resolution2 = common.getResolution()
        # set resolution monitor 1
        if "resolution" in values:
            if values["resolution"] == "auto":
                resolution = "auto"
        index = self.systemInputResolution.findText(resolution,
                                                        QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.systemInputResolution.setCurrentIndex(index)
        else:
            if resolution != "":
                self.systemInputResolution.addItem(resolution)
                
        # set resolution monitor 2
        if "resolution2" in values:
            if values["resolution2"] == "auto":
                resolution2 = "auto"

        index = self.systemInputResolution2.findText(resolution2,
                                                         QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.systemInputResolution2.setCurrentIndex(index)
        else:
            if resolution != "":
                self.systemInputResolution2.addItem(resolution2)
            
        # vpn
        vpnvalues = vpn.readVPN(self)
        if "ovpn" in vpnvalues:
            self.vpnInputovpn.setText(vpnvalues["ovpn"])
        if "parametervpn" in vpnvalues:
            self.vpnInputParameter.setText(vpnvalues["parametervpn"])
        if "systemlogin" in vpnvalues:
            if vpnvalues["systemlogin"] == "yes":
                self.vpnInputSystemLogin.setChecked(True)                
        if "autostartvpn" in vpnvalues:
            if vpnvalues["autostartvpn"] == "yes":
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
            
        system = common.getSystemTyp()
        if system != "PI4":
            self.systemInputArgon1.setEnabled(False)
            self.systemInputOneninedesign.setEnabled(False)
            
        # get sound cards
        values = common.getSoundCards()
        common.fillComboBoxList(self, values, self.systemInputSound)
        soundcard = common.getCurrentSoundCard()
        stringsplit = soundcard.split(" ")
        cardnumber = stringsplit[0].strip() + " "
        
        for index in range(self.systemInputSound.count()):
            value = self.systemInputSound.itemText(index)
            if value.startswith(cardnumber):
                self.systemInputSound.setCurrentIndex(index)
                break
        
        # set title
        self.setWindowTitle(common.getRessource("dialogTitle"))
        # Select first Tab
        self.thinClientTab.setCurrentIndex(0)
        # start vpn connection
        if autostartvpn:
            parameter = None
            systemlogin = None
            if "parametervpn" in vpnvalues:
                parameter = vpnvalues["parametervpn"]
            systemlogin = None
            if "systemlogin" in vpnvalues:
                systemlogin = vpnvalues["systemlogin"]
            vpn.autostartvpn(self, vpnvalues["ovpn"], parameter, systemlogin)
        # autostart connections
        self.autostart()
        # read existing connections
        self.fillListWidgets()
        # set passwort to "not changed"
        self.RemotePasswordChanged = False
        self.PasswordChanged = False
        self.sshPasswordChanged = False

    def changeText(self, index):
        self.text.setText(self.combo.itemText(index))
        
    def closeEvent(self, event):
        logging.info("close")
        common.systemShutdown(self)
        #event.ignore()

    def fillListWidgets(self):
        common.fillListWidgets(self, self.connectedThreads)

    def remotePasswordChanged(self):
        self.RemotePasswordChanged = True
        
    def passwordChanged(self):
        self.PasswordChanged = True
        
    def sshPasswordChanged(self):
        self.sshPasswordChanged = True

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
                    if "hostalive" in values:
                        if values["hostalive"] == "yes":
                            result = common.isHostAlive(values["address"])
                    else:
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
                connectionlog = common.getRessource("fileConnectionLog")
                # run connection as thread
                runconnect = connectThread.connectThread(command, connectionname, connectionlog)
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
# -------
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

# System
# ------
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

    def searchSSID(self):
        logging.info("searchSSID")
        values = common.getWlan()
        self.networkInputWlanSSID.clear()
        common.fillComboBoxList(self, values, self.networkInputWlanSSID)
        
    def systemReboot(self):
        common.systemReboot(self)

    def systemShutdown(self):
        common.systemShutdown(self)
     
    def connectionLog(self):
        common.connectionLog(self)
        
# vpn
# ---
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

    def vpnDeleteFile(self): 
        logging.info("vpnDeleteFile")
        vpn.vpnDeleteFile(self)

# save and restart
# ----------------
    def save(self):
        logging.info("save and restart")
        values = {}
        # check password
        if self.systemInputStartAdmin.isChecked() == False:
            password = self.systemInputPassword.text()
            values["adminPassword"] = password
            passwordrepeat = self.systemInputPasswordRepeat.text()
            if password == "":
                common.messageDialog("systemRemotePasswordError")
                return            
            if self.PasswordChanged:
                if password == passwordrepeat:
                    values["adminPassword"] = common.convertPassword(password)
                else:
                    common.messageDialog("systemPasswordComparisonError")
                    return

        # check remote vnc password
        if self.systemInputRemoteVNC.isChecked() and self.RemotePasswordChanged:
            vncpassword = self.systemInputRemotePassword.text()
            passwordrepeat = self.systemInputRemotePasswordRepeat.text()
            if vncpassword == "":
                common.messageDialog("systemRemotePasswordError")
                return            
            if vncpassword != passwordrepeat:
                common.messageDialog("systemPasswordComparisonError")
                return
            
        # check ssh password
        if self.systemInputSSH.isChecked() and self.sshPasswordChanged:
            sshpassword = self.systemInputsshPassword.text()
            passwordrepeat = self.systemInputsshPasswordRepeat.text()
            if sshpassword == "":
                common.messageDialog("systemsshPasswordError")
                return            
            if sshpassword != passwordrepeat:
                common.messageDialog("systemPasswordComparisonError")
                return
                
        # action time is string, convert to datetime or hour:minute
        value = self.timeInputActionTime.text()
        if value != "":
            # hour:minute
            if value.startswith("+"):
                value = value.replace("+", "")
                try:
                    time = datetime.strptime(value, "%H:%M")
                except ValueError as error:
                    common.messageDialog("timeActionError")
                    return
            else:
                try:
                    time = datetime.strptime(value, "%Y-%m-%d %H:%M")
                except ValueError as error:
                    common.messageDialog("timeActionError")
                    return
            
        # network
        if self.networkInputSave.isChecked() == False:
            networkvalues = {}
            networkvalues["connection"] = self.networkInputInterface.currentText()
            networkvalues["address"] = self.networkInputAddress.text()
            networkvalues["subnetmask"] = self.networkInputSubnetmask.text()
            networkvalues["gateway"] = self.networkInputGateway.text()
            networkvalues["dns"] = self.networkInputDNS.text()
            networkvalues["ssid"] = self.networkInputWlanSSID.currentText()
            networkvalues["password"] = self.networkInputWlanPassword.text()
            
            if self.networkInputDHCP.isChecked():
                common.networkWriteDHCP(networkvalues)
            else:
                result = common.networkWriteStaticIP(networkvalues)
                if not result:
                    return
           
        # vpn
        vpn.vpnTransfer(self)
        
        # system
        if self.systemInputStartAdmin.isChecked():
            values["startAdmin"] = "yes"
        else:
            values["startAdmin"] = "no"

        if self.systemInputRemoteVNC.isChecked():
            if self.RemotePasswordChanged:
                common.remoteVNC(True, vncpassword)
        else:
            common.remoteVNC(False, None)
            
        if self.systemInputSSH.isChecked():
            if self.sshPasswordChanged:
                common.remoteSSH(True, self.systemInputsshPassword.text())
        else:
            common.remoteSSH(False, None)
        
        values["resolution"] = self.systemInputResolution.currentText()
        values["resolution2"] = self.systemInputResolution2.currentText()
        
        orientation = "left"
        if self.systemInputMultiMonitorLeft.isChecked():
            orientation = "left"
        if self.systemInputMultiMonitorRight.isChecked():
            orientation = "right"
        if self.systemInputMultiMonitorAbove.isChecked():
            orientation = "above"
        if self.systemInputMultiMonitorBelow.isChecked():
            orientation = "below"
            
        common.setMultiMonitor(True, orientation)
                    
        values["language"] = self.systemInputLanguage.currentText()
        values["keyboardLayout"] = self.systemInputKeyboardLayout.currentText()
        
        values["startMinimized"] = "no"
        if self.systemInputMinimize.isChecked():
            values["startMinimized"] = "yes"
        
        values["networkSave"] = "yes"
        if self.networkInputSave.isChecked():
            values["networkSave"] = "no"
        # write system file
        common.writeSystem(values)
        
        common.writeKeyboardLayout(values["keyboardLayout"])
        # write system file        
        common.deleteConfigScript()
        
        if self.systemInputScreensaver.isChecked():
            common.setScreensaver("on")
        else:
            common.setScreensaver("off")
        if self.systemInputMonitorStandby.isChecked():
            common.setMonitorStandby("on")
        else:
            common.setMonitorStandby("off")
            
        common.deleteConfigScript()
        if self.systemInputScreensaver.isChecked():
            common.setScreensaver("on")
        else:
            common.setScreensaver("off")
            
        if self.systemInputMonitorStandby.isChecked():
            common.setMonitorStandby("on")
        else:
            common.setMonitorStandby("off")
            
        common.setResolution(self.systemInputResolution.currentText())
        
        if self.systemInputUSBAutomount.isChecked():
            common.setUSBAutomount("on")
        else:
            common.setUSBAutomount("off")
            
        if self.systemInputOneninedesign.isChecked():
            common.setOneninedesign("on")
        else:
            common.setOneninedesign("off")
            
        if self.systemInputArgon1.isChecked():
            common.setArgon1("on")
        else:
            common.setArgon1("off")            
                
        common.setSoundCard(self.systemInputSound.currentText())

        # write time
        values = {}
        values["save"] = "yes"
        if self.timeInputSave.isChecked():
            values["save"] = "no"
        values["automatic"] = "no"
        if self.timeInputAuto.isChecked():
            values["automatic"] = "yes"
        values["ntp"] = self.timeInputNTP.text()
        values["zone"] = self.timeInputTimezone.currentText()
        values["repeat"] = "no"
        if self.timeInputActionRepeat.isChecked():
            values["repeat"] = "yes"
        values["time"] = self.timeInputTime.text()
        values["execute"] = "no"
        if self.timeInputAction.isChecked():
            values["execute"] = "yes"
        values["action"] = self.timeInputActionAction.currentText()
        values["execat"] = self.timeInputActionTime.text()
        common.writeTime(values)
        
        # write time temp. file for save and reboot
        values = {}
        values["show"] = "no"
        if self.timeInputView.isChecked():
            values["show"] = "yes"
        common.writeTimeTemp(values)
        
        # reboot system
        result = common.confirmDialog(self,
                                      common.getRessource("systemShutdownTitle"),
                                      common.getRessource("systemAssumeMessage"))
        if result:
            command = common.getRessource("commandReboot")
            common.runProgram(command)


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
