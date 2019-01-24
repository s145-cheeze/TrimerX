# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Test.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from Triming import *
from AnsChk.Main import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 50)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setObjectName("pushButton_1")
        self.horizontalLayout.addWidget(self.pushButton_1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_2.raise_()
        self.pushButton_1.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionK = QtWidgets.QAction(MainWindow)
        self.actionK.setObjectName("actionK")
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "モード選択"))
        self.pushButton_1.setText(_translate("MainWindow", "トリミング"))
        self.pushButton_1.clicked.connect(self.GoTrimingWindow)
        self.pushButton_2.setText(_translate("MainWindow", "採点機能"))
        self.actionK.setText(_translate("MainWindow", "k"))
        self.pushButton_2.clicked.connect(self.GoAH)


    def GoAH(self,MainWindow):
        self.anschk = AnswerCheckMain()
        self.anschk.show()


    def GoTrimingWindow(self, MainWindow):
        self.widget = QtWidgets.QTabWidget()
        self.ui = Ui_tabWidget()
        self.ui.setupUi2(self.widget)
        self.widget.show()
