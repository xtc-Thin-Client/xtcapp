# -*- coding: iso-8859-1 -*-
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import common
import dialogrdesktopui
import logging


class dialogRDesktopUI(QtWidgets.QDialog, dialogrdesktopui.Ui_DialogRdesktop):

    connectionname = ""

    def __init__(self, name, configfile):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.connectionname = name
        # label
        common.setRessourceFile(configfile)
        self.setWindowTitle(common.getRessource("rdesktopDialogTitle"))
        self.rdesktopOKButton.setText(common.getRessource("ButtonOK"))
        self.rdesktopCancelButton.setText(common.getRessource("ButtonCancel"))
        self.rdesktopLabelName.setText(common.getRessource("configDialogLabelName"))
        self.rdesktopLabelAddress.setText(
                                          common.getRessource("configDialogLabelAddress"))
        self.rdesktopLabelResolution.setText(
                                             common.getRessource("configDialogLabelResolution"))
        self.rdesktopLabelColor.setText(
                                        common.getRessource("configDialogLabelColor"))
        self.rdesktopLabelParameter.setText(
                                            common.getRessource("configDialogLabelParameter"))
        self.rdesktopInputAutostart.setText(
                                            common.getRessource("configDialogLabelAutostart"))
        self.rdesktopInputRepeat.setText(
                                         common.getRessource("configDialogLabelRepeat"))
        self.rdesktopInputSystemLogin.setText(
                                              common.getRessource("configDialogLabelSystemLogin"))
        self.rdesktopLabelAlternative.setText(common.getRessource("configDialogLabelAlternative"))                                      
        self.rdesktopInputIcon.setText(
                                         common.getRessource("configDialogLabelIcon"))
        self.rdesktopLabelIconName.setText(
                                         common.getRessource("configDialogLabelIconName"))        
        #action
        self.rdesktopOKButton.clicked.connect(self.ButtonOK)
        self.rdesktopCancelButton.clicked.connect(self.ButtonCancel)
        # fill ComboBox
        common.fillComboBox(self, "rdesktopResolutions",
                            self.rdesktopInputResolution)
        common.fillComboBox(self, "rdesktopColorLevel", self.rdesktopInputColor)
        common.fillComboBoxConnections(self, self.rdesktopInputAlternative)

        if self.connectionname != "":
            # read connection parameter and fill dialog
            connection = common.readConnection(self.connectionname)
            self.rdesktopInputName.setText(self.connectionname)
            self.rdesktopInputAddress.setText(connection["address"])
            self.rdesktopInputParameter.setText(connection["parameter"])
            # Resolution
            index = self.rdesktopInputResolution.findText(connection["resolution"],
                                                          QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.rdesktopInputResolution.setCurrentIndex(index)
            # Color
            index = self.rdesktopInputColor.findText(connection["color"],
                                                     QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.rdesktopInputColor.setCurrentIndex(index)
            # Autostart
            autostart = connection["autostart"]
            if autostart == "yes":
                self.rdesktopInputAutostart.setChecked(True)
            # Repeat
            repeat = connection["repeat"]
            if repeat == "yes":
                self.rdesktopInputRepeat.setChecked(True)
            # Own Login
            systemlogin = connection["systemlogin"]
            if systemlogin == "yes":
                self.rdesktopInputSystemLogin.setChecked(True)
            # Alternative
            alternative = connection["alternative"]
            if alternative != "":
                index = self.rdesktopInputAlternative.findText(alternative, QtCore.Qt.MatchFixedString)
                self.rdesktopInputAlternative.setCurrentIndex(index)    
            # Icon
            icon = "no"
            if "icon" in connection:
                icon = connection["icon"]
            if icon == "yes":
                self.rdesktopInputIcon.setChecked(True)
            iconname = ""
            if "iconname" in connection:
                iconname = connection["iconname"]
            self.rdesktopInputIconName.setText(iconname)                

    def ButtonOK(self):
        logging.info("ButtonOK")
        error = False
        if self.rdesktopInputName.text() == "":
            common.messageDialog("configDialogErrorName")
            error = True
        elif " " in self.rdesktopInputName.text():
            common.messageDialog("configDialogErrorCharacter")
            error = True
        elif "[" in self.rdesktopInputName.text():
            common.messageDialog("configDialogErrorCharacter")
            error = True
        elif "]" in self.rdesktopInputName.text():
            common.messageDialog("configDialogErrorCharacter")
            error = True
        elif self.rdesktopInputAddress.text() == "":
            common.messageDialog("configDialogErrorAddress")
            error = True
        elif common.isNetworkAddress(self.rdesktopInputAddress.text()) is False:
            error = True
        elif self.rdesktopInputIcon.isChecked() and self.rdesktopInputIconName.text() == "":
            common.messageDialog("configDialogErrorIconName")
            error = True        

        name = self.rdesktopInputName.text()
        if common.existingConnection(name):
            common.messageDialog("configDialogErrorAddress")
            error = True

        if error is False:
            values = {}
            values["typ"] = "rdesktop"
            values["address"] = self.rdesktopInputAddress.text()
            values["resolution"] = self.rdesktopInputResolution.currentText()
            values["color"] = self.rdesktopInputColor.currentText()
            values["parameter"] = self.rdesktopInputParameter.text()
            if self.rdesktopInputAutostart.isChecked():
                values["autostart"] = "yes"
            else:
                values["autostart"] = "no"
            if self.rdesktopInputRepeat.isChecked():
                values["repeat"] = "yes"
            else:
                values["repeat"] = "no"
            if self.rdesktopInputSystemLogin.isChecked():
                values["systemlogin"] = "yes"
            else:
                values["systemlogin"] = "no"

            values["alternative"] = str(self.rdesktopInputAlternative.currentText())

            if self.rdesktopInputIcon.isChecked():
                values["icon"] = "yes"
            else:
                values["icon"] = "no"
            
            values["iconname"] = str(self.rdesktopInputIconName.text())
            
            # delete old connection
            if self.connectionname != "":
                common.deleteConnection(self.connectionname)
            # delete new connection
            common.deleteConnection(self.rdesktopInputName.text())
            # make new connection
            parameter = self.parameterRdesktop(self.rdesktopInputName.text(), values)
            common.newConnection(values, parameter, self.rdesktopInputName.text())
            self.close()

    def ButtonCancel(self):
        logging.info("ButtonCancel")
        self.close()

    def parameterRdesktop(self, connectionname, values):
        logging.info("parameterRdesktop")
        parameters = common.getRessource("commandRdesktop")
        parameters = parameters + " " + values["address"]
        if values["resolution"] == "FullScreen":
            parameters = parameters + " " + common.getRessource("rdesktopFullScreen")
        else:
            parameters = parameters + " " + common.getRessource("rdesktopScreen") + " " + values["resolution"]
        parameters = parameters + " " + common.getRessource("rdesktopColor") + " " + values["color"]        
        
        if values["systemlogin"] == "yes":
            parameters = parameters + " " + common.getRessource("rdesktopUser") + " " + common.getRessource("commandPlaceholderUser")
            parameters = parameters + " " + common.getRessource("rdesktopPassword") + " " + common.getRessource("commandPlaceholderPassword")

        if values["parameter"] != "":
            parameters = parameters + " " + values["parameter"]
            
        logging.info(parameters)
        return parameters

