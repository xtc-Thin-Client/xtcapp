# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialoglogin.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogLogin(object):
    def setupUi(self, DialogLogin):
        DialogLogin.setObjectName("DialogLogin")
        DialogLogin.resize(400, 190)
        self.formLayoutWidget = QtWidgets.QWidget(DialogLogin)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 81))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.loginLabelLogin = QtWidgets.QLabel(self.formLayoutWidget)
        self.loginLabelLogin.setObjectName("loginLabelLogin")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.loginLabelLogin)
        self.loginInputLogin = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.loginInputLogin.setObjectName("loginInputLogin")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.loginInputLogin)
        self.loginLabelPassword = QtWidgets.QLabel(self.formLayoutWidget)
        self.loginLabelPassword.setObjectName("loginLabelPassword")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.loginLabelPassword)
        self.loginInputPassword = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.loginInputPassword.setInputMethodHints(QtCore.Qt.ImhNone)
        self.loginInputPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginInputPassword.setObjectName("loginInputPassword")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.loginInputPassword)
        self.horizontalLayoutWidget = QtWidgets.QWidget(DialogLogin)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 100, 381, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loginButtonOK = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.loginButtonOK.setObjectName("loginButtonOK")
        self.horizontalLayout.addWidget(self.loginButtonOK)
        self.loginButtonCancel = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.loginButtonCancel.setObjectName("loginButtonCancel")
        self.horizontalLayout.addWidget(self.loginButtonCancel)

        self.retranslateUi(DialogLogin)
        QtCore.QMetaObject.connectSlotsByName(DialogLogin)

    def retranslateUi(self, DialogLogin):
        _translate = QtCore.QCoreApplication.translate
        DialogLogin.setWindowTitle(_translate("DialogLogin", "Login"))
        self.loginLabelLogin.setText(_translate("DialogLogin", "Anwendername"))
        self.loginLabelPassword.setText(_translate("DialogLogin", "Passwort"))
        self.loginButtonOK.setText(_translate("DialogLogin", "OK"))
        self.loginButtonCancel.setText(_translate("DialogLogin", "Abbrechen"))
