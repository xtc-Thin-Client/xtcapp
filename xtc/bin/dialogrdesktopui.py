# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogrdesktop.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogRdesktop(object):
    def setupUi(self, DialogRdesktop):
        DialogRdesktop.setObjectName("DialogRdesktop")
        DialogRdesktop.resize(647, 509)
        self.formLayoutWidget = QtWidgets.QWidget(DialogRdesktop)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 631, 381))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.rdesktopLabelName = QtWidgets.QLabel(self.formLayoutWidget)
        self.rdesktopLabelName.setObjectName("rdesktopLabelName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.rdesktopLabelName)
        self.rdesktopInputName = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.rdesktopInputName.setObjectName("rdesktopInputName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.rdesktopInputName)
        self.rdesktopLabelAddress = QtWidgets.QLabel(self.formLayoutWidget)
        self.rdesktopLabelAddress.setObjectName("rdesktopLabelAddress")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.rdesktopLabelAddress)
        self.rdesktopInputAddress = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.rdesktopInputAddress.setObjectName("rdesktopInputAddress")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.rdesktopInputAddress)
        self.rdesktopLabelResolution = QtWidgets.QLabel(self.formLayoutWidget)
        self.rdesktopLabelResolution.setObjectName("rdesktopLabelResolution")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.rdesktopLabelResolution)
        self.rdesktopInputResolution = QtWidgets.QComboBox(self.formLayoutWidget)
        self.rdesktopInputResolution.setObjectName("rdesktopInputResolution")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.rdesktopInputResolution)
        self.rdesktopLabelColor = QtWidgets.QLabel(self.formLayoutWidget)
        self.rdesktopLabelColor.setObjectName("rdesktopLabelColor")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.rdesktopLabelColor)
        self.rdesktopInputColor = QtWidgets.QComboBox(self.formLayoutWidget)
        self.rdesktopInputColor.setObjectName("rdesktopInputColor")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.rdesktopInputColor)
        self.rdesktopLabelParameter = QtWidgets.QLabel(self.formLayoutWidget)
        self.rdesktopLabelParameter.setObjectName("rdesktopLabelParameter")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.rdesktopLabelParameter)
        self.rdesktopInputParameter = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.rdesktopInputParameter.setObjectName("rdesktopInputParameter")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.rdesktopInputParameter)
        self.rdesktopInputSystemLogin = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.rdesktopInputSystemLogin.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.rdesktopInputSystemLogin.setObjectName("rdesktopInputSystemLogin")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.rdesktopInputSystemLogin)
        self.rdesktopInputAutostart = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.rdesktopInputAutostart.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.rdesktopInputAutostart.setObjectName("rdesktopInputAutostart")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.rdesktopInputAutostart)
        self.rdesktopInputRepeat = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.rdesktopInputRepeat.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.rdesktopInputRepeat.setObjectName("rdesktopInputRepeat")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.rdesktopInputRepeat)
        self.rdesktopLabelAlternative = QtWidgets.QLabel(self.formLayoutWidget)
        self.rdesktopLabelAlternative.setObjectName("rdesktopLabelAlternative")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.rdesktopLabelAlternative)
        self.rdesktopInputAlternative = QtWidgets.QComboBox(self.formLayoutWidget)
        self.rdesktopInputAlternative.setObjectName("rdesktopInputAlternative")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.rdesktopInputAlternative)
        self.horizontalLayoutWidget = QtWidgets.QWidget(DialogRdesktop)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 410, 631, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rdesktopOKButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rdesktopOKButton.sizePolicy().hasHeightForWidth())
        self.rdesktopOKButton.setSizePolicy(sizePolicy)
        self.rdesktopOKButton.setObjectName("rdesktopOKButton")
        self.horizontalLayout.addWidget(self.rdesktopOKButton)
        self.rdesktopCancelButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rdesktopCancelButton.sizePolicy().hasHeightForWidth())
        self.rdesktopCancelButton.setSizePolicy(sizePolicy)
        self.rdesktopCancelButton.setObjectName("rdesktopCancelButton")
        self.horizontalLayout.addWidget(self.rdesktopCancelButton)

        self.retranslateUi(DialogRdesktop)
        QtCore.QMetaObject.connectSlotsByName(DialogRdesktop)

    def retranslateUi(self, DialogRdesktop):
        _translate = QtCore.QCoreApplication.translate
        DialogRdesktop.setWindowTitle(_translate("DialogRdesktop", "rdesktop"))
        self.rdesktopLabelName.setText(_translate("DialogRdesktop", "Name"))
        self.rdesktopLabelAddress.setText(_translate("DialogRdesktop", "Adresse"))
        self.rdesktopLabelResolution.setText(_translate("DialogRdesktop", "Auflösung"))
        self.rdesktopLabelColor.setText(_translate("DialogRdesktop", "Farbtiefe"))
        self.rdesktopLabelParameter.setText(_translate("DialogRdesktop", "Weitere Parameter"))
        self.rdesktopInputSystemLogin.setText(_translate("DialogRdesktop", "Eigenes Login"))
        self.rdesktopInputAutostart.setText(_translate("DialogRdesktop", "Automatisch starten"))
        self.rdesktopInputRepeat.setText(_translate("DialogRdesktop", "Neu verbinden"))
        self.rdesktopLabelAlternative.setText(_translate("DialogRdesktop", "Alternativ"))
        self.rdesktopOKButton.setText(_translate("DialogRdesktop", "OK"))
        self.rdesktopCancelButton.setText(_translate("DialogRdesktop", "Abbrechen"))
