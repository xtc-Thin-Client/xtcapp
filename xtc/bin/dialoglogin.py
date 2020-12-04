# -*- coding: iso-8859-1 -*-
import dialogloginui
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import logging
import common


class dialogLoginUI(QtWidgets.QDialog, dialogloginui.Ui_DialogLogin):

    def __init__(self, configfile, title):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        # label
        common.setRessourceFile(configfile)
        self.setWindowTitle(title)
        self.loginButtonOK.setText(common.getRessource("ButtonOK"))
        self.loginButtonCancel.setText(common.getRessource("ButtonCancel"))
        self.loginLabelLogin.setText(common.getRessource("systemLabelLogin"))
        self.loginLabelPassword.setText(common.getRessource("systemLabelPassword"))
        #action
        self.loginButtonOK.clicked.connect(self.ButtonOK)
        self.loginButtonCancel.clicked.connect(self.ButtonCancel)

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

    def getLogin(self):
        return self.loginInputLogin.text()
    
    def getPassword(self):
        return self.loginInputPassword.text()
