# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Triming.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from FreeTrim.FreeTrimMain import *

class Ui_tabWidget(object):
    def setupUi2(self, tabWidget):
        tabWidget.setObjectName("tabWidget")
        tabWidget.resize(400, 154)
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        tabWidget.addTab(self.tab, "")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.tab1)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        tabWidget.addTab(self.tab1, "")

        self.retranslateUi(tabWidget)
        tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(tabWidget)

    def retranslateUi(self, tabWidget):
        _translate = QtCore.QCoreApplication.translate
        tabWidget.setWindowTitle(_translate("tabWidget", "TabWidget"))
        self.label.setText(_translate("tabWidget", "説明文"))
        self.pushButton.setText(_translate("tabWidget", "PushButton"))
        self.pushButton.clicked.connect(self.GoFreeTrimingWindow)
        tabWidget.setTabText(tabWidget.indexOf(self.tab), _translate("tabWidget", "自由トリミング"))
        self.label_2.setText(_translate("tabWidget", "説明文"))
        self.pushButton_2.setText(_translate("tabWidget", "PushButton"))
        tabWidget.setTabText(tabWidget.indexOf(self.tab1), _translate("tabWidget", "固定トリミング"))

    def GoFreeTrimingWindow(self, tabWidet):
        self.widget = QtWidgets()
        self.ui = FreeTrimMain()
        self.ui.initUI(self.widget)
        self.widget.show()
