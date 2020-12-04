# -*- coding: iso-8859-1 -*-
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import common
import dialogsshui
import logging

class dialogsshUI(QtWidgets.QDialog, dialogsshui.Ui_Dialogssh):

    connectionname = ""

    def __init__(self, name, configfile):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.connectionname = name
        # label
        common.setRessourceFile(configfile)
        self.setWindowTitle(common.getRessource("sshDialogTitle"))
        self.sshOKButton.setText(common.getRessource("ButtonOK"))
        self.sshCancelButton.setText(common.getRessource("ButtonCancel"))
        self.sshLabelName.setText(common.getRessource("configDialogLabelName"))
        self.sshLabelAddress.setText(common.getRessource("configDialogLabelAddress"))
        self.sshLabelPort.setText(common.getRessource("configDialogLabelPort"))
        self.sshLabelLogin.setText(common.getRessource("configDialogLabelLogin"))
        self.sshLabelApplication.setText(common.getRessource("configDialogLabelApplication"))
        self.sshLabelPassword.setText(common.getRessource("configDialogLabelPassword"))
        self.sshLabelParameter.setText(common.getRessource("configDialogLabelParameter"))
        self.sshInputRepeat.setText(common.getRessource("configDialogLabelRepeat"))
        self.sshLabelAlternative.setText(common.getRessource("configDialogLabelAlternative"))
        # action
        self.sshOKButton.clicked.connect(self.ButtonOK)
        self.sshCancelButton.clicked.connect(self.ButtonCancel)
        # fill comboBox
        common.fillComboBoxConnections(self, self.sshInputAlternative)

        if self.connectionname != "":
            # read connection parameter and fill dialog
            connection = common.readConnection(self.connectionname)
            self.sshInputName.setText(self.connectionname)
            self.sshInputAddress.setText(connection["address"])
            self.sshInputPort.setText(connection["port"])
            self.sshInputLogin.setText(connection["login"])
            self.sshInputApplication.setText(connection["application"])
            self.sshInputPassword.setText(connection["password"])
            self.sshInputParameter.setText(connection["parameter"])
            autostart = connection["autostart"]
            if autostart == "yes":
                self.sshInputAutostart.setChecked(True)
            # Repeat
            repeat = connection["repeat"]
            if repeat == "yes":
                self.sshInputRepeat.setChecked(True)
            # Alternative
            alternative = connection["alternative"]
            if alternative != "":
                index = self.sshInputAlternative.findText(alternative, QtCore.Qt.MatchFixedString)
                self.sshInputAlternative.setCurrentIndex(index)    

    def ButtonOK(self):
        logging.info("ButtonOK")
        error = False
        if self.sshInputName.text() == "":
            common.messageDialog("configDialogErrorName")
            error = True
        elif self.sshInputAddress.text() == "":
            common.messageDialog("configDialogErrorAddress")
            error = True
        elif self.sshInputLogin.text() == "":
            common.messageDialog("configDialogErrorLogin")
            error = True
        elif self.sshInputApplication.text() == "":
            common.messageDialog("configDialogErrorApplication")
            error = True
        elif self.sshInputPassword.text() == "":
            common.messageDialog("configDialogErrorPassword")
            error = True

        name = self.sshInputName.text()
        if common.existingConnection(name):
            common.messageDialog("configDialogErrorAddress")
            error = True

        if error == False:
            values = {}
            values["typ"] = "ssh"
            values["name"] = self.sshInputName.text()
            values["address"] = self.sshInputAddress.text()
            values["port"] = self.sshInputPort.text()
            values["login"] = self.sshInputLogin.text()
            values["application"] = self.sshInputApplication.text()
            values["password"] = self.sshInputPassword.text()
            values["parameter"] = self.sshInputParameter.text()
            if self.sshInputAutostart.isChecked():
                values["autostart"] = "yes"
            else:
                values["autostart"] = "no"
            if self.sshInputRepeat.isChecked():
                values["repeat"] = "yes"
            else:
                values["repeat"] = "no"

            values["alternative"] = str(self.sshInputAlternative.currentText())

            # delete old connection
            if self.connectionname != "":
                common.deleteConnection(self.connectionname)
                common.deletePasswordFile(self.connectionname)
            # delete new connection
            common.deleteConnection(self.sshInputName.text())
            common.deletePasswordFile(self.sshInputName.text())
            # make new connection
            parameter = self.parameterssh(self.sshInputName.text(), values)
            common.newConnection(values, parameter, self.sshInputName.text())
            self.close()

    def ButtonCancel(self):
        logging.info("ButtonCancel")
        self.close()

    def newPasswordFile(self, connectionname, password):
        logging.info("writePasswordFile")
        filename = common.getRessource("passwordFile") + "." + connectionname
        filew = fopen(filename, "w")
        filew.write(password)
        filew.close()
        return filename

    def parameterssh(self, connectionname, values):
        logging.info("parameterssh")
        parameters = ""
        if values["password"] != "":
            parameters = common.getRessource("commandsshpass")
            parameters = parameters + " \'" + values["password"] + "\' "
        parameters = parameters + common.getRessource("commandssh")
        parameters = parameters + " " + values["address"]
        parameters = parameters + " " + common.getRessource("sshLoginName") + " " + values["login"]
        if values["port"] != "":
            parameters = parameters + " " + common.getRessource("sshPort") + " " + values["port"]
        if values["application"] != "":
            parameters = parameters + " " + values["application"]
        if values["parameter"] != "":
            parameters = parameters + " " + values["parameter"]
        logging.info(parameters)
        return parameters

