# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets, QtGui

from PyQt5.QtCore import QDir, QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QImage, QImageWriter, QPainter, QPen, qRgb
from PyQt5.QtWidgets import (QAction, QApplication, QColorDialog, QFileDialog,
        QInputDialog, QMainWindow, QMenu, QMessageBox, QWidget)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter

from TPaintWidget import *

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex1 = FreeTrim()
    ex1.show()
    sys.exit(app.exec_())


class FreeTrimRect(object):
        """docstring for FreeTrimRect."""
        def __init__(self, *args):
            super(FreeTrimRect, self).__init__()
            self.update(*args)
        def get(self):
            return self.p1, self.p2
        def update(self,*args):
            if len(args) == 4:
                self.p1 = args[0], args[1]
                self.p2 = args[2], args[3]
            elif len(args) == 2:
                self.p1 = args[0]
                self.p2 = args[1]
        def __str__(self):
            return "FreeTrimRect<{},{}>".format(str(self.p1), str(self.p2))


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
