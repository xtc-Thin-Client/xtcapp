# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'run.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_run(object):
    def setupUi(self, run):
        run.setObjectName("run")
        run.resize(170, 76)
        self.centralwidget = QtWidgets.QWidget(run)
        self.centralwidget.setObjectName("centralwidget")
        run.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(run)
        self.statusbar.setObjectName("statusbar")
        run.setStatusBar(self.statusbar)

        self.retranslateUi(run)
        QtCore.QMetaObject.connectSlotsByName(run)

    def retranslateUi(self, run):
        _translate = QtCore.QCoreApplication.translate
        run.setWindowTitle(_translate("run", "run"))
