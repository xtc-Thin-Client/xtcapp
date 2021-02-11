from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import subprocess
import logging


class connectThread(QtCore.QThread):
    command = None
    name = None
    pid = None
    process = None
    threadCancel = pyqtSignal(str)

    def __init__(self, command, name, connectionlog):
        super(connectThread, self).__init__()
        self.command = command
        self.name = name
        self.connectionlog = connectionlog
        
    def run(self):
        try:
            global result
            logging.info(self.command)
            #self.process = subprocess.Popen(self.command, shell=True,
            #stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.process = subprocess.Popen(self.command, shell=True,
            stdout=subprocess.PIPE, stderr=open(self.connectionlog, "a"))
            self.pid = self.process.pid
            self.process.communicate()
            logging.info("end")
            self.threadCancel.emit(self.name)
        except OSError as error:
            logging.error(error)

    def getPid(self):
        return self.pid

    def getName(self):
        return self.name
