# -*- coding: iso-8859-1 -*-
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import common
import dialogx2goui
import logging

class dialogx2goUI(QtWidgets.QDialog, dialogx2goui.Ui_Dialogx2go):
    
    connectionname = ""

    def __init__(self, name, configfile):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.connectionname = name
        # label
        common.setRessourceFile(configfile)
        self.setWindowTitle(common.getRessource("x2goDialogTitle"))
        self.x2goOKButton.setText(common.getRessource("ButtonOK"))
        self.x2goCancelButton.setText(common.getRessource("ButtonCancel"))
        self.x2goLabelName.setText(common.getRessource("configDialogLabelName"))
        self.x2goLabelAddress.setText(common.getRessource("configDialogLabelAddress"))
        self.x2goLabelUser.setText(common.getRessource("configDialogLabelUser"))
        self.x2goLabelPassword.setText(common.getRessource("configDialogLabelPassword"))
        self.x2goLabelKeyboard.setText(common.getRessource("configDialogLabelKeyboard"))
        self.x2goLabelResolution.setText(common.getRessource("configDialogLabelResolution"))
        self.x2goLabelDesktop.setText(common.getRessource("configDialogLabelDesktop"))
        self.x2goLabelParameter.setText(common.getRessource("configDialogLabelParameter"))
        self.x2goInputRepeat.setText(common.getRessource("configDialogLabelRepeat"))
        self.x2goLabelAlternative.setText(common.getRessource("configDialogLabelAlternative"))
        self.x2goInputSystemLogin.setText(common.getRessource("configDialogLabelSystemLogin"))
        # fill ComboBox
        common.fillComboBox(self, "x2goResolutions", self.x2goInputResolution)
        common.fillComboBox(self, "x2goKeyboardLayout", self.x2goInputKeyboard)
        common.fillComboBox(self, "x2goDesktop", self.x2goInputDesktop)
        common.fillComboBoxConnections(self, self.x2goInputAlternative)
        # action
        self.x2goOKButton.clicked.connect(self.ButtonOK)
        self.x2goCancelButton.clicked.connect(self.ButtonCancel)

        if self.connectionname != "":
            # read connection parameter and fill dialog
            connection = common.readConnection(self.connectionname)
            self.x2goInputName.setText(self.connectionname)
            self.x2goInputAddress.setText(connection["address"])
            self.x2goInputUser.setText(connection["user"])
            self.x2goInputPassword.setText(connection["password"])
            self.x2goInputParameter.setText(connection["parameter"])
            # Keyboard layout
            index = self.x2goInputKeyboard.findText(connection["keyboard"],
                                                    QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.x2goInputKeyboard.setCurrentIndex(index)
            # Resolution
            index = self.x2goInputResolution.findText(connection["resolution"],
                                                      QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.x2goInputResolution.setCurrentIndex(index)
            # Desktop
            index = self.x2goInputDesktop.findText(connection["desktop"],
                                                   QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.x2goInputDesktop.setCurrentIndex(index)
            # Own Login
            systemlogin = connection["systemlogin"]
            if systemlogin == "yes":
                self.x2goInputSystemLogin.setChecked(True)
            # Autostart
            autostart = connection["autostart"]
            if autostart == "yes":
                self.x2goInputAutostart.setChecked(True)
            # Repeat
            repeat = connection["repeat"]
            if repeat == "yes":
                self.x2goInputRepeat.setChecked(True)
            # Alternative
            alternative = connection["alternative"]
            if alternative != "":
                index = self.x2goInputAlternative.findText(alternative, QtCore.Qt.MatchFixedString)
                self.x2goInputAlternative.setCurrentIndex(index)    

    def ButtonOK(self):
        logging.info("ButtonOK")
        error = False
        if self.x2goInputName.text() == "":
            common.messageDialog("configDialogErrorName")
            error = True
        elif self.x2goInputAddress.text() == "":
            common.messageDialog("configDialogErrorAddress")
            error = True

        name = self.x2goInputName.text()
        if common.existingConnection(name):
            common.messageDialog("configDialogErrorAddress")
            error = True

        if error == False:
            values = {}
            values["typ"] = "x2go"
            values["name"] = self.x2goInputName.text()
            values["address"] = self.x2goInputAddress.text()
            values["user"] = self.x2goInputUser.text()
            values["password"] = self.x2goInputPassword.text()
            values["parameter"] = self.x2goInputParameter.text()
            values["resolution"] = self.x2goInputResolution.currentText()
            values["keyboard"] = self.x2goInputKeyboard.currentText()
            values["desktop"] = self.x2goInputDesktop.currentText()
            if self.x2goInputAutostart.isChecked():
                values["autostart"] = "yes"
            else:
                values["autostart"] = "no"                
                
            if self.x2goInputRepeat.isChecked():
                values["repeat"] = "yes"
            else:
                values["repeat"] = "no"

            if self.x2goInputSystemLogin.isChecked():
                values["systemlogin"] = "yes"
            else:
                values["systemlogin"] = "no"
                
            values["alternative"] = str(self.x2goInputAlternative.currentText())

            # delete old connection
            if self.connectionname != "":
                common.deleteConnection(self.connectionname)
                common.deletePasswordFile(self.connectionname)
            # delete new connection
            common.deleteConnection(self.x2goInputName.text())
            common.deletePasswordFile(self.x2goInputName.text())
            # make new connection
            parameter = self.parameterx2go(self.x2goInputName.text(), values)
            common.newConnection(values, parameter, self.x2goInputName.text())
            self.close()

    def ButtonCancel(self):
        logging.info("ButtonCancel")
        self.close()

    def parameterx2go(self, connectionname, values):
        logging.info("parameterx2go")
        parameters = ""
        parameters = parameters + common.getRessource("commandx2go")
        parameters = parameters + " " + common.getRessource("x2goServer") + " " + values["address"]
        parameters = parameters + " " + common.getRessource("x2goNew")
        parameters = parameters + " " + common.getRessource("x2goCommand") + " " + values["desktop"]
        parameters = parameters + " " + common.getRessource("x2goKeyboard") + " " + values["keyboard"]
        parameters = parameters + " " + common.getRessource("x2goResolution") + " " + values["resolution"]
        if values["systemlogin"] == "yes":
            parameters = parameters + " " + common.getRessource("x2goUser") + " " + common.getRessource("commandPlaceholderUser")
            parameters = parameters + " " + common.getRessource("x2goPassword") + " " + common.getRessource("commandPlaceholderPassword")
        else:
            parameters = parameters + " " + common.getRessource("x2goUser") + " " + values["user"]
            parameters = parameters + " " + common.getRessource("x2goPassword") + " " + values["password"]        
        
        if values["parameter"] != "":
            parameters = parameters + " " + values["parameter"]
        logging.info(parameters)
        return parameters

