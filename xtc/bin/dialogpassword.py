# -*- coding: iso-8859-1 -*-
import dialogpasswordui
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import logging
import common


class dialogPasswordUI(QtWidgets.QDialog, dialogpasswordui.Ui_DialogPassword):

    def __init__(self, configfile):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        # label
        common.setRessourceFile(configfile)
        self.passwordOKButton.setText(common.getRessource("ButtonOK"))
        self.passwordCancelButton.setText(common.getRessource("ButtonCancel"))
        self.passwordLabelPassword.setText(common.getRessource("systemLabelPassword"))
        #action
        self.passwordOKButton.clicked.connect(self.ButtonOK)
        self.passwordCancelButton.clicked.connect(self.ButtonCancel)

    def ButtonOK(self):
        logging.info("ButtonOK")
        self.result = True
        self.close()

    def ButtonCancel(self):
        logging.info("ButtonCancel")
        self.result = False
        self.close()

    def getResult(self):
        return self.result

    def getPassword(self):
        return self.passwordInputPassword.text()