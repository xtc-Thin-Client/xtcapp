# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogtigervnc.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogTigerVNC(object):
    def setupUi(self, DialogTigerVNC):
        DialogTigerVNC.setObjectName("DialogTigerVNC")
        DialogTigerVNC.resize(646, 510)
        self.formLayoutWidget = QtWidgets.QWidget(DialogTigerVNC)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 621, 381))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.vncLabelName = QtWidgets.QLabel(self.formLayoutWidget)
        self.vncLabelName.setObjectName("vncLabelName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.vncLabelName)
        self.vncInputName = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.vncInputName.setObjectName("vncInputName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.vncInputName)
        self.vncLabelAddress = QtWidgets.QLabel(self.formLayoutWidget)
        self.vncLabelAddress.setObjectName("vncLabelAddress")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.vncLabelAddress)
        self.vncInputAddress = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.vncInputAddress.setObjectName("vncInputAddress")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.vncInputAddress)
        self.vncLabelPort = QtWidgets.QLabel(self.formLayoutWidget)
        self.vncLabelPort.setObjectName("vncLabelPort")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.vncLabelPort)
        self.vncInputPort = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.vncInputPort.setObjectName("vncInputPort")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.vncInputPort)
        self.vncLabelPassword = QtWidgets.QLabel(self.formLayoutWidget)
        self.vncLabelPassword.setObjectName("vncLabelPassword")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.vncLabelPassword)
        self.vncInputPassword = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.vncInputPassword.setObjectName("vncInputPassword")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.vncInputPassword)
        self.vncLabelResolution = QtWidgets.QLabel(self.formLayoutWidget)
        self.vncLabelResolution.setObjectName("vncLabelResolution")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.vncLabelResolution)
        self.vncInputResolution = QtWidgets.QComboBox(self.formLayoutWidget)
        self.vncInputResolution.setObjectName("vncInputResolution")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.vncInputResolution)
        self.vncLabelColor = QtWidgets.QLabel(self.formLayoutWidget)
        self.vncLabelColor.setObjectName("vncLabelColor")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.vncLabelColor)
        self.vncInputColor = QtWidgets.QComboBox(self.formLayoutWidget)
        self.vncInputColor.setObjectName("vncInputColor")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.vncInputColor)
        self.vncInputAutostart = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.vncInputAutostart.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.vncInputAutostart.setObjectName("vncInputAutostart")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.vncInputAutostart)
        self.vncLabelParameter = QtWidgets.QLabel(self.formLayoutWidget)
        self.vncLabelParameter.setObjectName("vncLabelParameter")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.vncLabelParameter)
        self.vncInputParameter = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.vncInputParameter.setObjectName("vncInputParameter")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.vncInputParameter)
        self.vncInputRepeat = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.vncInputRepeat.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.vncInputRepeat.setObjectName("vncInputRepeat")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.vncInputRepeat)
        self.vncLabelAlternative = QtWidgets.QLabel(self.formLayoutWidget)
        self.vncLabelAlternative.setObjectName("vncLabelAlternative")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.vncLabelAlternative)
        self.vncInputAlternative = QtWidgets.QComboBox(self.formLayoutWidget)
        self.vncInputAlternative.setObjectName("vncInputAlternative")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.vncInputAlternative)
        self.horizontalLayoutWidget = QtWidgets.QWidget(DialogTigerVNC)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 410, 621, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.vncOKButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vncOKButton.sizePolicy().hasHeightForWidth())
        self.vncOKButton.setSizePolicy(sizePolicy)
        self.vncOKButton.setObjectName("vncOKButton")
        self.horizontalLayout.addWidget(self.vncOKButton)
        self.vncCancelButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vncCancelButton.sizePolicy().hasHeightForWidth())
        self.vncCancelButton.setSizePolicy(sizePolicy)
        self.vncCancelButton.setObjectName("vncCancelButton")
        self.horizontalLayout.addWidget(self.vncCancelButton)

        self.retranslateUi(DialogTigerVNC)
        QtCore.QMetaObject.connectSlotsByName(DialogTigerVNC)
        DialogTigerVNC.setTabOrder(self.vncInputName, self.vncInputAddress)
        DialogTigerVNC.setTabOrder(self.vncInputAddress, self.vncInputPort)
        DialogTigerVNC.setTabOrder(self.vncInputPort, self.vncInputPassword)
        DialogTigerVNC.setTabOrder(self.vncInputPassword, self.vncInputResolution)
        DialogTigerVNC.setTabOrder(self.vncInputResolution, self.vncInputColor)
        DialogTigerVNC.setTabOrder(self.vncInputColor, self.vncInputParameter)
        DialogTigerVNC.setTabOrder(self.vncInputParameter, self.vncInputAutostart)
        DialogTigerVNC.setTabOrder(self.vncInputAutostart, self.vncOKButton)
        DialogTigerVNC.setTabOrder(self.vncOKButton, self.vncCancelButton)

    def retranslateUi(self, DialogTigerVNC):
        _translate = QtCore.QCoreApplication.translate
        DialogTigerVNC.setWindowTitle(_translate("DialogTigerVNC", "TigerVNC"))
        self.vncLabelName.setText(_translate("DialogTigerVNC", "Name"))
        self.vncLabelAddress.setText(_translate("DialogTigerVNC", "Adresse"))
        self.vncLabelPort.setText(_translate("DialogTigerVNC", "Port"))
        self.vncLabelPassword.setText(_translate("DialogTigerVNC", "Passwort"))
        self.vncLabelResolution.setText(_translate("DialogTigerVNC", "Auflösung"))
        self.vncLabelColor.setText(_translate("DialogTigerVNC", "Farbtiefe"))
        self.vncInputAutostart.setText(_translate("DialogTigerVNC", "Automatisch starten"))
        self.vncLabelParameter.setText(_translate("DialogTigerVNC", "Weitere Parameter"))
        self.vncInputRepeat.setText(_translate("DialogTigerVNC", "Neu verbinden"))
        self.vncLabelAlternative.setText(_translate("DialogTigerVNC", "Alternativ"))
        self.vncOKButton.setText(_translate("DialogTigerVNC", "OK"))
        self.vncCancelButton.setText(_translate("DialogTigerVNC", "Abbrechen"))
