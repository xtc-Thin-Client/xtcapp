# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogpassword.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogPassword(object):
    def setupUi(self, DialogPassword):
        DialogPassword.setObjectName("DialogPassword")
        DialogPassword.resize(400, 128)
        self.horizontalLayoutWidget = QtWidgets.QWidget(DialogPassword)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 60, 351, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.passwordOKButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.passwordOKButton.setObjectName("passwordOKButton")
        self.horizontalLayout.addWidget(self.passwordOKButton)
        self.passwordCancelButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.passwordCancelButton.setObjectName("passwordCancelButton")
        self.horizontalLayout.addWidget(self.passwordCancelButton)
        self.formLayoutWidget = QtWidgets.QWidget(DialogPassword)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 351, 41))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.passwordLabelPassword = QtWidgets.QLabel(self.formLayoutWidget)
        self.passwordLabelPassword.setObjectName("passwordLabelPassword")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.passwordLabelPassword)
        self.passwordInputPassword = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.passwordInputPassword.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.passwordInputPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordInputPassword.setObjectName("passwordInputPassword")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.passwordInputPassword)

        self.retranslateUi(DialogPassword)
        QtCore.QMetaObject.connectSlotsByName(DialogPassword)
        DialogPassword.setTabOrder(self.passwordInputPassword, self.passwordOKButton)
        DialogPassword.setTabOrder(self.passwordOKButton, self.passwordCancelButton)

    def retranslateUi(self, DialogPassword):
        _translate = QtCore.QCoreApplication.translate
        DialogPassword.setWindowTitle(_translate("DialogPassword", "Passwort"))
        self.passwordOKButton.setText(_translate("DialogPassword", "OK"))
        self.passwordCancelButton.setText(_translate("DialogPassword", "Abbrechen"))
        self.passwordLabelPassword.setText(_translate("DialogPassword", "Paswort"))
