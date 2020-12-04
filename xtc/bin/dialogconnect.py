# -*- coding: iso-8859-1 -*-
import dialogconnectui
import common
from PyQt5 import *

connectionname = ""

class dialogConnectUI(QtGui.QDialog, dialogconnectui.Ui_connectDialog):

    def __init__(self, configfile):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        # label
        common.setRessourceFile(configfile)
        self.connectCancelButton.setText(common.getRessource("ButtonCancel"))
        self.connectLabel.setText(common.getRessource("connectDialogConnection"))

