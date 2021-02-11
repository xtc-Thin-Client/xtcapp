# -*- coding: iso-8859-1 -*-
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import common
import dialogtigervncui
import logging

class dialogTigerVNCUI(QtWidgets.QDialog, dialogtigervncui.Ui_DialogTigerVNC):
    
    connectionname = ""
    
    def __init__(self, name, configfile):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.connectionname = name
        # label
        common.setRessourceFile(configfile)
        self.setWindowTitle(common.getRessource("TigerVNCViewerDialogTitle"))
        self.vncOKButton.setText(common.getRessource("ButtonOK"))
        self.vncCancelButton.setText(common.getRessource("ButtonCancel"))
        self.vncLabelName.setText(common.getRessource("configDialogLabelName"))
        self.vncLabelAddress.setText(common.getRessource("configDialogLabelAddress"))
        self.vncLabelPort.setText(common.getRessource("configDialogLabelPort"))
        self.vncLabelPassword.setText(common.getRessource("configDialogLabelPassword"))
        self.vncLabelResolution.setText(common.getRessource("configDialogLabelResolution"))
        self.vncLabelColor.setText(common.getRessource("configDialogLabelColor"))
        self.vncLabelParameter.setText(common.getRessource("configDialogLabelParameter"))
        self.vncInputAutostart.setText(common.getRessource("configDialogLabelAutostart"))
        self.vncInputRepeat.setText(common.getRessource("configDialogLabelRepeat"))
        self.vncLabelAlternative.setText(common.getRessource("configDialogLabelAlternative"))        
        self.vncInputIcon.setText(common.getRessource("configDialogLabelIcon"))
        self.vncLabelIconName.setText(common.getRessource("configDialogLabelIconName"))        
        #action
        self.vncOKButton.clicked.connect(self.ButtonOK)
        self.vncCancelButton.clicked.connect(self.ButtonCancel)
        # fill ComboBox
        common.fillComboBox(self, "VNCResolutions", self.vncInputResolution)
        common.fillComboBox(self, "TigerVNCViewerColorLevel", self.vncInputColor)
        common.fillComboBoxConnections(self, self.vncInputAlternative)

        if self.connectionname != "":
            # read connection parameter and fill dialog
            connection = common.readConnection(self.connectionname)
            self.vncInputName.setText(self.connectionname)
            self.vncInputAddress.setText(connection["address"])
            self.vncInputPort.setText(connection["port"])
            self.vncInputPassword.setText(connection["password"])
            self.vncInputParameter.setText(connection["parameter"])
            # Resolution
            index = self.vncInputResolution.findText(connection["resolution"],
                                                     QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.vncInputResolution.setCurrentIndex(index)
            # Color
            index = self.vncInputColor.findText(connection["color"],
                                                QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.vncInputColor.setCurrentIndex(index)
            # Autostart
            autostart = connection["autostart"]
            if autostart == "yes":
                self.vncInputAutostart.setChecked(True)
            # Repeat
            repeat = connection["repeat"]
            if repeat == "yes":
                self.vncInputRepeat.setChecked(True)
            # Alternative
            alternative = connection["alternative"]
            if alternative != "":
                index = self.vncInputAlternative.findText(alternative, QtCore.Qt.MatchFixedString)
                self.vncInputAlternative.setCurrentIndex(index)    
            # Icon
            icon = "no"
            if "icon" in connection:
                icon = connection["icon"]
            if icon == "yes":
                self.vncInputIcon.setChecked(True)
            iconname = ""
            if "iconname" in connection:
                iconname = connection["iconname"]
            self.vncInputIconName.setText(iconname)
                
    def ButtonOK(self):
        logging.info("ButtonOK")
        error = False
        if self.vncInputName.text() == "":
            common.messageDialog("configDialogErrorName")
            error = True
        elif " " in self.vncInputName.text():
            common.messageDialog("configDialogErrorCharacter")
            error = True
        elif "[" in self.vncInputName.text():
            common.messageDialog("configDialogErrorCharacter")
            error = True
        elif "]" in self.vncInputName.text():
            common.messageDialog("configDialogErrorCharacter")
            error = True
        elif self.vncInputAddress.text() == "":
            common.messageDialog("configDialogErrorAddress")
            error = True
        elif self.vncInputPort.text() == "":
            common.messageDialog("configDialogErrorPort")
            error = True
        elif common.isNetworkAddress(self.vncInputAddress.text()) == False:
            error = True
        elif self.vncInputIcon.isChecked() and self.vncInputIconName.text() == "":
            common.messageDialog("configDialogErrorIconName")
            error = True
            
        name = self.vncInputName.text()
        if common.existingConnection(name):
            common.messageDialog("configDialogErrorAddress")
            error = True

        if error == False:
            values = {}
            values["typ"] = "vnc"
            values["address"] = self.vncInputAddress.text()
            values["port"] = self.vncInputPort.text()
            values["password"] = self.vncInputPassword.text()
            values["resolution"] = self.vncInputResolution.currentText()
            values["color"] = self.vncInputColor.currentText()
            values["parameter"] = self.vncInputParameter.text()
            if self.vncInputAutostart.isChecked():
                values["autostart"] = "yes"
            else:
                values["autostart"] = "no"
            if self.vncInputRepeat.isChecked():
                values["repeat"] = "yes"
            else:
                values["repeat"] = "no"
                
            values["alternative"] = str(self.vncInputAlternative.currentText())
            
            if self.vncInputIcon.isChecked():
                values["icon"] = "yes"
            else:
                values["icon"] = "no"
            
            values["iconname"] = str(self.vncInputIconName.text())
            
            # delete old connection
            if self.connectionname != "":
                common.deleteConnection(self.connectionname)
                common.deletePasswordFile(self.connectionname)
            # delete new connection
            common.deleteConnection(self.vncInputName.text())
            common.deletePasswordFile(self.vncInputName.text())
            # make new connection
            parameter = self.parameterVNC(self.vncInputName.text(), values)
            common.newConnection(values, parameter, self.vncInputName.text())
            password = self.vncInputPassword.text()
            if password != "":
                self.newPasswordFile(self.vncInputName.text(), password)
            self.close()

    def ButtonCancel(self):
        logging.info("ButtonCancel")
        self.close()

    def newPasswordFile(self, connectionname, password):
        logging.info("writePasswordFile")
        filename = common.getRessource("passwordFile") + "." + connectionname
        command = common.getRessource("commandVNCPasswd")
        common.runProgram("echo '" + password + "' | " + command + " " + filename)

    def parameterVNC(self, connectionname, values):
        logging.info("parameterVNC")
        parameters = common.getRessource("commandVNCViewer")
        parameters = parameters + " " + values["address"] + ":" + values["port"]
        if values["password"] != "":
            parameters = parameters + " " + common.getRessource("TigerVNCViewerPassword") + " " + common.getPasswordFile(connectionname)

        if values["resolution"] == "FullScreen":
            parameters = parameters + " " + common.getRessource("TigerVNCViewerFullScreen")
        else:
            parameters = parameters + " " + common.getRessource("TigerVNCViewerScreen") + " " + values["resolution"]
        if values["color"] == "FullColor":
            parameters = parameters + " " + common.getRessource("TigerVNCViewerFullColor")
        else:
            parameters = parameters + " " + common.getRessource("TigerVNCViewerColor") + " " + values["color"]
        if values["parameter"] != "":
            parameters = parameters + " " + values["parameter"]
        logging.info(parameters)
        return parameters

