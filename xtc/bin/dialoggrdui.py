# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogrdp.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DialogRDP(object):
    def setupUi(self, DialogRDP):
        DialogRDP.setObjectName(_fromUtf8("DialogRDP"))
        DialogRDP.resize(646, 510)
        self.formLayoutWidget = QtGui.QWidget(DialogRDP)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 20, 631, 381))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.rdpLabelName = QtGui.QLabel(self.formLayoutWidget)
        self.rdpLabelName.setObjectName(_fromUtf8("rdpLabelName"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.rdpLabelName)
        self.rdpInputName = QtGui.QLineEdit(self.formLayoutWidget)
        self.rdpInputName.setObjectName(_fromUtf8("rdpInputName"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.rdpInputName)
        self.rdpLabelAddress = QtGui.QLabel(self.formLayoutWidget)
        self.rdpLabelAddress.setObjectName(_fromUtf8("rdpLabelAddress"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.rdpLabelAddress)
        self.rdpInputAddress = QtGui.QLineEdit(self.formLayoutWidget)
        self.rdpInputAddress.setObjectName(_fromUtf8("rdpInputAddress"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.rdpInputAddress)
        self.rdpLabelResolution = QtGui.QLabel(self.formLayoutWidget)
        self.rdpLabelResolution.setObjectName(_fromUtf8("rdpLabelResolution"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.rdpLabelResolution)
        self.rdpInputResolution = QtGui.QComboBox(self.formLayoutWidget)
        self.rdpInputResolution.setObjectName(_fromUtf8("rdpInputResolution"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.rdpInputResolution)
        self.rdpLabelColor = QtGui.QLabel(self.formLayoutWidget)
        self.rdpLabelColor.setObjectName(_fromUtf8("rdpLabelColor"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.rdpLabelColor)
        self.rdpInputColor = QtGui.QComboBox(self.formLayoutWidget)
        self.rdpInputColor.setObjectName(_fromUtf8("rdpInputColor"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.rdpInputColor)
        self.rdpInputAutostart = QtGui.QCheckBox(self.formLayoutWidget)
        self.rdpInputAutostart.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.rdpInputAutostart.setObjectName(_fromUtf8("rdpInputAutostart"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.rdpInputAutostart)
        self.rdpLabelParameter = QtGui.QLabel(self.formLayoutWidget)
        self.rdpLabelParameter.setObjectName(_fromUtf8("rdpLabelParameter"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.rdpLabelParameter)
        self.rdpInputParameter = QtGui.QLineEdit(self.formLayoutWidget)
        self.rdpInputParameter.setObjectName(_fromUtf8("rdpInputParameter"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.rdpInputParameter)
        self.rdpInputRepeat = QtGui.QCheckBox(self.formLayoutWidget)
        self.rdpInputRepeat.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.rdpInputRepeat.setObjectName(_fromUtf8("rdpInputRepeat"))
        self.formLayout.setWidget(10, QtGui.QFormLayout.LabelRole, self.rdpInputRepeat)
        self.rdpLabelUser = QtGui.QLabel(self.formLayoutWidget)
        self.rdpLabelUser.setObjectName(_fromUtf8("rdpLabelUser"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.rdpLabelUser)
        self.rdpInputUser = QtGui.QLineEdit(self.formLayoutWidget)
        self.rdpInputUser.setObjectName(_fromUtf8("rdpInputUser"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.rdpInputUser)
        self.rdpLabelPassword = QtGui.QLabel(self.formLayoutWidget)
        self.rdpLabelPassword.setObjectName(_fromUtf8("rdpLabelPassword"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.rdpLabelPassword)
        self.rdpInputPassword = QtGui.QLineEdit(self.formLayoutWidget)
        self.rdpInputPassword.setObjectName(_fromUtf8("rdpInputPassword"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.rdpInputPassword)
        self.horizontalLayoutWidget = QtGui.QWidget(DialogRDP)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 410, 621, 80))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.rdpOKButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rdpOKButton.sizePolicy().hasHeightForWidth())
        self.rdpOKButton.setSizePolicy(sizePolicy)
        self.rdpOKButton.setObjectName(_fromUtf8("rdpOKButton"))
        self.horizontalLayout.addWidget(self.rdpOKButton)
        self.rdpCancelButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rdpCancelButton.sizePolicy().hasHeightForWidth())
        self.rdpCancelButton.setSizePolicy(sizePolicy)
        self.rdpCancelButton.setObjectName(_fromUtf8("rdpCancelButton"))
        self.horizontalLayout.addWidget(self.rdpCancelButton)

        self.retranslateUi(DialogRDP)
        QtCore.QMetaObject.connectSlotsByName(DialogRDP)
        DialogRDP.setTabOrder(self.rdpInputName, self.rdpInputAddress)
        DialogRDP.setTabOrder(self.rdpInputAddress, self.rdpInputResolution)
        DialogRDP.setTabOrder(self.rdpInputResolution, self.rdpInputColor)
        DialogRDP.setTabOrder(self.rdpInputColor, self.rdpInputParameter)
        DialogRDP.setTabOrder(self.rdpInputParameter, self.rdpInputAutostart)
        DialogRDP.setTabOrder(self.rdpInputAutostart, self.rdpOKButton)
        DialogRDP.setTabOrder(self.rdpOKButton, self.rdpCancelButton)

    def retranslateUi(self, DialogRDP):
        DialogRDP.setWindowTitle(_translate("DialogRDP", "RDP", None))
        self.rdpLabelName.setText(_translate("DialogRDP", "Name", None))
        self.rdpLabelAddress.setText(_translate("DialogRDP", "Adresse", None))
        self.rdpLabelResolution.setText(_translate("DialogRDP", "Auflösung", None))
        self.rdpLabelColor.setText(_translate("DialogRDP", "Farbtiefe", None))
        self.rdpInputAutostart.setText(_translate("DialogRDP", "Automatisch starten", None))
        self.rdpLabelParameter.setText(_translate("DialogRDP", "Weitere Parameter", None))
        self.rdpInputRepeat.setText(_translate("DialogRDP", "Neu verbinden", None))
        self.rdpLabelUser.setText(_translate("DialogRDP", "Anwendername", None))
        self.rdpLabelPassword.setText(_translate("DialogRDP", "Passwort", None))
        self.rdpOKButton.setText(_translate("DialogRDP", "OK", None))
        self.rdpCancelButton.setText(_translate("DialogRDP", "Abbrechen", None))

