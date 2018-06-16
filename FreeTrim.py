# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QFileDialog

from TPaintWidget import *

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex1 = FreeTrim()
    ex1.show()
    sys.exit(app.exec_())



class FreeTrim(TPaintWidget):
    def __init__(self, parent=None):
        super(FreeTrim, self).__init__(parent)
        self.fname = self.showDialog()

        self.hbox = QtWidgets.QHBoxLayout(self)
        self.pixmap = QtGui.QPixmap(self.fname[0])
        self.lbl = QtWidgets.QLabel(self)
        self.lbl.setPixmap(self.pixmap)

        self.hbox.addWidget(self.lbl)
        self.setLayout(self.hbox)

    def showDialog(self):
        return QFileDialog.getOpenFileName(parent = self, caption = "OpenFile" , filter ='*.jpg' )



if __name__ == '__main__':
    main()
