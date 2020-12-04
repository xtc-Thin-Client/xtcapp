# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogconnect.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_connectDialog(object):
    def setupUi(self, connectDialog):
        connectDialog.setObjectName("connectDialog")
        connectDialog.resize(393, 135)
        self.connectLabel = QtWidgets.QLabel(connectDialog)
        self.connectLabel.setGeometry(QtCore.QRect(30, 30, 331, 20))
        self.connectLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.connectLabel.setObjectName("connectLabel")
        self.connectCancelButton = QtWidgets.QPushButton(connectDialog)
        self.connectCancelButton.setGeometry(QtCore.QRect(150, 70, 88, 34))
        self.connectCancelButton.setObjectName("connectCancelButton")

        self.retranslateUi(connectDialog)
        QtCore.QMetaObject.connectSlotsByName(connectDialog)

    def retranslateUi(self, connectDialog):
        _translate = QtCore.QCoreApplication.translate
        connectDialog.setWindowTitle(_translate("connectDialog", "Verbinde"))
        self.connectLabel.setText(_translate("connectDialog", "TextLabel"))
        self.connectCancelButton.setText(_translate("connectDialog", "Abbrechen"))
