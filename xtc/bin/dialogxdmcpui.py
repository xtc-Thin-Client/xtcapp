# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogxdmcp.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogXdmcp(object):
    def setupUi(self, DialogXdmcp):
        DialogXdmcp.setObjectName("DialogXdmcp")
        DialogXdmcp.resize(479, 443)
        self.formLayoutWidget = QtWidgets.QWidget(DialogXdmcp)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 451, 291))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.xdmcpLabelAddress = QtWidgets.QLabel(self.formLayoutWidget)
        self.xdmcpLabelAddress.setObjectName("xdmcpLabelAddress")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.xdmcpLabelAddress)
        self.xdmcpInputAddress = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.xdmcpInputAddress.setObjectName("xdmcpInputAddress")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.xdmcpInputAddress)
        self.xdmcpLabelPort = QtWidgets.QLabel(self.formLayoutWidget)
        self.xdmcpLabelPort.setObjectName("xdmcpLabelPort")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.xdmcpLabelPort)
        self.xdmcpInputPort = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.xdmcpInputPort.setObjectName("xdmcpInputPort")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.xdmcpInputPort)
        self.xdmcpInputAutostart = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.xdmcpInputAutostart.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.xdmcpInputAutostart.setObjectName("xdmcpInputAutostart")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.xdmcpInputAutostart)
        self.xdmcpLabelName = QtWidgets.QLabel(self.formLayoutWidget)
        self.xdmcpLabelName.setObjectName("xdmcpLabelName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.xdmcpLabelName)
        self.xdmcpInputName = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.xdmcpInputName.setObjectName("xdmcpInputName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.xdmcpInputName)
        self.xdmcpLabelParameter = QtWidgets.QLabel(self.formLayoutWidget)
        self.xdmcpLabelParameter.setObjectName("xdmcpLabelParameter")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.xdmcpLabelParameter)
        self.xdmcpInputParameter = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.xdmcpInputParameter.setObjectName("xdmcpInputParameter")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.xdmcpInputParameter)
        self.xdmcpLabelResolution = QtWidgets.QLabel(self.formLayoutWidget)
        self.xdmcpLabelResolution.setObjectName("xdmcpLabelResolution")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.xdmcpLabelResolution)
        self.xdmcpInputResolution = QtWidgets.QComboBox(self.formLayoutWidget)
        self.xdmcpInputResolution.setObjectName("xdmcpInputResolution")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.xdmcpInputResolution)
        self.xdmcpInputRepeat = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.xdmcpInputRepeat.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.xdmcpInputRepeat.setObjectName("xdmcpInputRepeat")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.xdmcpInputRepeat)
        self.xdmcpLabelAlternative = QtWidgets.QLabel(self.formLayoutWidget)
        self.xdmcpLabelAlternative.setObjectName("xdmcpLabelAlternative")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.xdmcpLabelAlternative)
        self.xdmcpInputAlternative = QtWidgets.QComboBox(self.formLayoutWidget)
        self.xdmcpInputAlternative.setObjectName("xdmcpInputAlternative")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.xdmcpInputAlternative)
        self.horizontalLayoutWidget = QtWidgets.QWidget(DialogXdmcp)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 330, 451, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.xdmcpOKButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xdmcpOKButton.sizePolicy().hasHeightForWidth())
        self.xdmcpOKButton.setSizePolicy(sizePolicy)
        self.xdmcpOKButton.setObjectName("xdmcpOKButton")
        self.horizontalLayout.addWidget(self.xdmcpOKButton)
        self.xdmcpCancelButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xdmcpCancelButton.sizePolicy().hasHeightForWidth())
        self.xdmcpCancelButton.setSizePolicy(sizePolicy)
        self.xdmcpCancelButton.setObjectName("xdmcpCancelButton")
        self.horizontalLayout.addWidget(self.xdmcpCancelButton)

        self.retranslateUi(DialogXdmcp)
        QtCore.QMetaObject.connectSlotsByName(DialogXdmcp)
        DialogXdmcp.setTabOrder(self.xdmcpInputName, self.xdmcpInputAddress)
        DialogXdmcp.setTabOrder(self.xdmcpInputAddress, self.xdmcpInputPort)
        DialogXdmcp.setTabOrder(self.xdmcpInputPort, self.xdmcpInputResolution)
        DialogXdmcp.setTabOrder(self.xdmcpInputResolution, self.xdmcpInputParameter)
        DialogXdmcp.setTabOrder(self.xdmcpInputParameter, self.xdmcpInputAutostart)
        DialogXdmcp.setTabOrder(self.xdmcpInputAutostart, self.xdmcpOKButton)
        DialogXdmcp.setTabOrder(self.xdmcpOKButton, self.xdmcpCancelButton)

    def retranslateUi(self, DialogXdmcp):
        _translate = QtCore.QCoreApplication.translate
        DialogXdmcp.setWindowTitle(_translate("DialogXdmcp", "XDMCP"))
        self.xdmcpLabelAddress.setText(_translate("DialogXdmcp", "Adresse"))
        self.xdmcpLabelPort.setText(_translate("DialogXdmcp", "Port"))
        self.xdmcpInputAutostart.setText(_translate("DialogXdmcp", "Automatisch starten"))
        self.xdmcpLabelName.setText(_translate("DialogXdmcp", "Name"))
        self.xdmcpLabelParameter.setText(_translate("DialogXdmcp", "Weitere Parameter"))
        self.xdmcpLabelResolution.setText(_translate("DialogXdmcp", "Auflösung"))
        self.xdmcpInputRepeat.setText(_translate("DialogXdmcp", "Neu verbinden"))
        self.xdmcpLabelAlternative.setText(_translate("DialogXdmcp", "Alternative"))
        self.xdmcpOKButton.setText(_translate("DialogXdmcp", "OK"))
        self.xdmcpCancelButton.setText(_translate("DialogXdmcp", "Abbrechen"))
