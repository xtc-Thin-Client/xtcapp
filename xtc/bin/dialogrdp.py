# -*- coding: iso-8859-1 -*-
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import common
import dialogrdpui
import logging


class dialogRDPUI(QtWidgets.QDialog, dialogrdpui.Ui_DialogRDP):

    connectionname = ""

    def __init__(self, name, configfile):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.connectionname = name
        # label
        common.setRessourceFile(configfile)
        self.setWindowTitle(common.getRessource("RDPViewerDialogTitle"))
        self.rdpOKButton.setText(common.getRessource("ButtonOK"))
        self.rdpCancelButton.setText(common.getRessource("ButtonCancel"))
        self.rdpLabelName.setText(common.getRessource("configDialogLabelName"))
        self.rdpLabelAddress.setText(
                                     common.getRessource("configDialogLabelAddress"))
        self.rdpLabelResolution.setText(
                                        common.getRessource("configDialogLabelResolution"))
        self.rdpLabelColor.setText(
                                   common.getRessource("configDialogLabelColor"))
        self.rdpLabelParameter.setText(
                                       common.getRessource("configDialogLabelParameter"))
        self.rdpInputAutostart.setText(
                                       common.getRessource("configDialogLabelAutostart"))
        self.rdpInputRepeat.setText(
                                    common.getRessource("configDialogLabelRepeat"))
        self.rdpInputSystemLogin.setText(
                                         common.getRessource("configDialogLabelSystemLogin"))
        self.rdpLabelAlternative.setText(
                                         common.getRessource("configDialogLabelAlternative"))    
        #action
        self.rdpOKButton.clicked.connect(self.ButtonOK)
        self.rdpCancelButton.clicked.connect(self.ButtonCancel)
        # fill ComboBox
        common.fillComboBox(self, "RDPViewerResolutions",
                            self.rdpInputResolution)
        common.fillComboBox(self, "RDPViewerColorLevel", self.rdpInputColor)
        common.fillComboBoxConnections(self, self.rdpInputAlternative)        
            
        if self.connectionname != "":
            # read connection parameter and fill dialog
            connection = common.readConnection(self.connectionname)
            self.rdpInputName.setText(self.connectionname)
            self.rdpInputAddress.setText(connection["address"])
            self.rdpInputParameter.setText(connection["parameter"])
            # Resolution
            index = self.rdpInputResolution.findText(connection["resolution"],
                                                     QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.rdpInputResolution.setCurrentIndex(index)
            # Color
            index = self.rdpInputColor.findText(connection["color"],
                                                QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.rdpInputColor.setCurrentIndex(index)
            # Autostart
            autostart = connection["autostart"]
            if autostart == "yes":
                self.rdpInputAutostart.setChecked(True)
            # Repeat
            repeat = connection["repeat"]
            if repeat == "yes":
                self.rdpInputRepeat.setChecked(True)
            # Own Login
            systemlogin = connection["systemlogin"]
            if systemlogin == "yes":
                self.rdpInputSystemLogin.setChecked(True)
            # Alternative
            alternative = connection["alternative"]
            if alternative != "":
                index = self.rdpInputAlternative.findText(alternative, QtCore.Qt.MatchFixedString)
                self.rdpInputAlternative.setCurrentIndex(index)    

    def ButtonOK(self):
        logging.info("ButtonOK")
        error = False
        if self.rdpInputName.text() == "":
            common.messageDialog("configDialogErrorName")
            error = True
        elif " " in self.rdpInputName.text():
            common.messageDialog("configDialogErrorCharacter")
            error = True
        elif "[" in self.rdpInputName.text():
            common.messageDialog("configDialogErrorCharacter")
            error = True
        elif "]" in self.rdpInputName.text():
            common.messageDialog("configDialogErrorCharacter")
            error = True
        elif self.rdpInputAddress.text() == "":
            common.messageDialog("configDialogErrorAddress")
            error = True
        elif common.isNetworkAddress(self.rdpInputAddress.text()) is False:
            error = True

        name = self.rdpInputName.text()
        if common.existingConnection(name):
            common.messageDialog("configDialogErrorAddress")
            error = True

        if error is False:
            values = {}
            values["typ"] = "rdp"
            values["address"] = self.rdpInputAddress.text()
            values["resolution"] = self.rdpInputResolution.currentText()
            values["color"] = self.rdpInputColor.currentText()
            values["parameter"] = self.rdpInputParameter.text()
            if self.rdpInputAutostart.isChecked():
                values["autostart"] = "yes"
            else:
                values["autostart"] = "no"
            if self.rdpInputRepeat.isChecked():
                values["repeat"] = "yes"
            else:
                values["repeat"] = "no"
            if self.rdpInputSystemLogin.isChecked():
                values["systemlogin"] = "yes"
            else:
                values["systemlogin"] = "no"

            values["alternative"] = str(self.rdpInputAlternative.currentText())
            
            # delete old connection
            if self.connectionname != "":
                common.deleteConnection(self.connectionname)
            # delete new connection
            common.deleteConnection(self.rdpInputName.text())
            # make new connection
            parameter = self.parameterRDP(self.rdpInputName.text(), values)
            common.newConnection(values, parameter, self.rdpInputName.text())
            self.close()

    def ButtonCancel(self):
        logging.info("ButtonCancel")
        self.close()

    def parameterRDP(self, connectionname, values):
        logging.info("parameterRDP")
        parameters = common.getRessource("commandRDPViewer")
        parameters = parameters + " " + common.getRessource("RDPViewerServer") + values["address"]
        if values["resolution"] == "FullScreen":
            parameters = parameters + " " + common.getRessource("RDPViewerFullScreen")
        else:
            parameters = parameters + " " + common.getRessource("RDPViewerScreen") + values["resolution"]
        parameters = parameters + " " + common.getRessource("RDPViewerColor") + values["color"]
        
        if values["systemlogin"] == "yes":
            parameters = parameters + " " + common.getRessource("RDPViewerUser") + common.getRessource("commandPlaceholderUser")
            parameters = parameters + " " + common.getRessource("RDPViewerPassword") + common.getRessource("commandPlaceholderPassword")
            
        if values["parameter"] != "":
            parameters = parameters + " " + values["parameter"]
        logging.info(parameters)
        return parameters

