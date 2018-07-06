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

        self.setAttribute(Qt.WA_StaticContents)
        self.modified = False
        self.scribbling = False
        self.myPenWidth = 1
        self.myPenColor = Qt.blue
        self.image = QImage()
        self.lastPoint = QPoint()

        self.minX = 0
        self.minY = 0
        self.maxX = 0
        self.maxY = 0

        self.currentRect = FreeTrimRect(self.minX, self.minY, self.maxX, self.maxY)
        self.rects = []

        self.openImage(self.fname[0])

    def updateRectByXY(self, x, y):
        self.minX = min(self.minX, x)
        self.minY = min(self.minY, y)
        self.maxX = max(self.maxX, x)
        self.maxY = max(self.maxY, y)
        self.currentRect.update(self.minX, self.minY, self.maxX, self.maxY)

    def updateRectByQPoint(self, pos):
        self.updateRectByXY(pos.x(), pos.y())


    def newRect(self):
        self.minX = 0
        self.minY = 0
        self.maxX = 0
        self.maxY = 0

        self.rects.append(self.currentRect)

        self.currentRect = FreeTrimRect(self.minX, self.minY, self.maxX, self.maxY)


    def showDialog(self):
        return QFileDialog.getOpenFileName(parent = self, caption = "OpenFile" , filter ='*.jpg' )

    def openImage(self, fileName):
        loadedImage = QImage()
        if not loadedImage.load(fileName):
            return False

        newSize = loadedImage.size().expandedTo(self.size())
        self.resizeImage(loadedImage, newSize)
        self.image = loadedImage
        self.modified = False
        self.update()
        return True

    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return

        newImage = QImage(newSize, QImage.Format_RGB32)
        newImage.fill(qRgb(255, 255, 255))
        painter = QPainter(newImage)
        painter.drawImage(QPoint(0, 0), image)
        self.image = newImage

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()
            self.scribbling = True
            self.updateRectByQPoint(event.pos())

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.scribbling:
            self.drawLineTo(event.pos())
            print(event.pos())
            print(event.pos().x(), event.pos().y())
            self.updateRectByQPoint(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.scribbling:
            self.drawLineTo(event.pos())
            self.scribbling = False
            self.updateRectByQPoint(event.pos())

    def paintEvent(self, event):
        painter = QPainter(self)
        dirtyRect = event.rect()
        painter.drawImage(dirtyRect, self.image, dirtyRect)


    def drawLineTo(self, endPoint):
        painter = QPainter(self.image)
        painter.setPen(QPen(self.myPenColor, self.myPenWidth, Qt.SolidLine,
        Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.lastPoint, endPoint)
        self.modified = True

        rad = self.myPenWidth / 2 + 2
        self.update(QRect(self.lastPoint, endPoint).normalized().adjusted(-rad, -rad, +rad, +rad))
        self.lastPoint = QPoint(endPoint)

if __name__ == '__main__':
    main()
