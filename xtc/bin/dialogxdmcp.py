# -*- coding: iso-8859-1 -*-
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import common
import dialogxdmcpui
import logging

class dialogxdmcpUI(QtWidgets.QDialog, dialogxdmcpui.Ui_DialogXdmcp):

    connectionname = ""

    def __init__(self, name, configfile):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.connectionname = name
        # label
        common.setRessourceFile(configfile)
        self.setWindowTitle(common.getRessource("xdmcpDialogTitle"))
        self.xdmcpOKButton.setText(common.getRessource("ButtonOK"))
        self.xdmcpCancelButton.setText(common.getRessource("ButtonCancel"))
        self.xdmcpLabelName.setText(common.getRessource("configDialogLabelName"))
        self.xdmcpLabelAddress.setText(common.getRessource("configDialogLabelAddress"))
        self.xdmcpLabelPort.setText(common.getRessource("configDialogLabelPort"))
        self.xdmcpLabelResolution.setText(common.getRessource("configDialogLabelResolution"))
        self.xdmcpLabelParameter.setText(common.getRessource("configDialogLabelParameter"))
        self.xdmcpInputRepeat.setText(common.getRessource("configDialogLabelRepeat"))
        self.xdmcpLabelAlternative.setText(common.getRessource("configDialogLabelAlternative"))
        # fill ComboBox
        common.fillComboBox(self, "xdmcpResolutions", self.xdmcpInputResolution)
        common.fillComboBoxConnections(self, self.xdmcpInputAlternative)
        # action
        self.xdmcpOKButton.clicked.connect(self.ButtonOK)
        self.xdmcpCancelButton.clicked.connect(self.ButtonCancel)

        if self.connectionname != "":
            # read connection parameter and fill dialog
            connection = common.readConnection(self.connectionname)
            self.xdmcpInputName.setText(self.connectionname)
            self.xdmcpInputAddress.setText(connection["address"])
            self.xdmcpInputPort.setText(connection["port"])
            self.xdmcpInputParameter.setText(connection["parameter"])
            # Resolution
            index = self.xdmcpInputResolution.findText(connection["resolution"],
                                                       QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.xdmcpInputResolution.setCurrentIndex(index)
            autostart = connection["autostart"]
            # Autostart
            if autostart == "yes":
                self.xdmcpInputAutostart.setChecked(True)
            # Repeat
            repeat = connection["repeat"]
            if repeat == "yes":
                self.x2goInputRepeat.setChecked(True)
            # Alternative
            alternative = connection["alternative"]
            if alternative != "":
                index = self.xdmcpInputAlternative.findText(alternative, QtCore.Qt.MatchFixedString)
                self.xdmcpInputAlternative.setCurrentIndex(index)    

    def ButtonOK(self):
        logging.info("ButtonOK")
        error = False
        if self.xdmcpInputName.text() == "":
            common.messageDialog("configDialogErrorName")
            error = True
        elif self.xdmcpInputAddress.text() == "":
            common.messageDialog("configDialogErrorAddress")
            error = True

        name = self.xdmcpInputName.text()
        if common.existingConnection(name):
            common.messageDialog("configDialogErrorAddress")
            error = True

        if error == False:
            values = {}
            values["typ"] = "xdmcp"
            values["name"] = self.xdmcpInputName.text()
            values["address"] = self.xdmcpInputAddress.text()
            values["port"] = self.xdmcpInputPort.text()
            values["resolution"] = self.xdmcpInputResolution.currentText()
            values["parameter"] = self.xdmcpInputParameter.text()
            if self.xdmcpInputAutostart.isChecked():
                values["autostart"] = "yes"
            else:
                values["autostart"] = "no"
            if self.xdmcpInputRepeat.isChecked():
                values["repeat"] = "yes"
            else:
                values["repeat"] = "no"

            values["alternative"] = str(self.xdmcpInputAlternative.currentText())

            # delete old connectio
            if self.connectionname != "":
                common.deleteConnection(self.connectionname)
                common.deletePasswordFile(self.connectionname)
            # delete new connection
            common.deleteConnection(self.xdmcpInputName.text())
            common.deletePasswordFile(self.xdmcpInputName.text())
            # make new connection
            parameter = self.parameterxdmcp(self.xdmcpInputName.text(), values)
            common.newConnection(values, parameter, self.xdmcpInputName.text())
            self.close()

    def ButtonCancel(self):
        logging.info("ButtonCancel")
        self.close()

    def parameterxdmcp(self, connectionname, values):
        logging.info("parameterxdmcp")
        parameters = ""
        parameters = parameters + common.getRessource("commandxdmcp")
        parameters = parameters + " " + values["address"]
        if values["port"] != "":
            parameters = parameters + " " + common.getRessource("xdmcpPort") + values["port"]
        if values["resolution"] == "fullscreen":
            parameters = parameters + " " + common.getRessource("xdmcpFullScreen")
        else:
            parameters = parameters + " " + common.getRessource("xdmcpResolution") + " " + values["resolution"]

        if values["parameter"] != "":
            parameters = parameters + " " + values["parameter"]
        logging.info(parameters)
        return parameters

