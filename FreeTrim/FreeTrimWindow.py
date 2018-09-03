# -*- coding: utf-8 -*-

import sys
from copy import deepcopy

import cv2

from PyQt5 import QtWidgets, QtGui

from PyQt5.QtCore import QDir, QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QImage, QImageWriter, QPainter, QPen, qRgb
from PyQt5.QtWidgets import (QAction, QApplication, QColorDialog, QFileDialog,
        QInputDialog, QMainWindow, QMenu, QMessageBox, QWidget)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter

from TPaintWidget import *

from FreeTrimRect import *
from FreeTrimRectData import *
from FreeTrimImage import *
from FreeTrimImageData import *



class FreeTrimWindow(TPaintWidget):
    def __init__(self, parent=None):
        super(FreeTrimWindow, self).__init__(parent)
        self.fname = self.showDialog()
        print(f"fname:{self.fname}")

        self.hbox = QtWidgets.QHBoxLayout(self)
        self.setLayout(self.hbox)

        self.setAttribute(Qt.WA_StaticContents)
        self.modified = False
        self.scribbling = False
        self.myPenWidth = 1
        self.myPenColor = Qt.blue
        self.image = QImage()
        self.lastPoint = QPoint()

        self.rectData = FreeTrimRectData()
        self.imgData = FreeTrimImageData()

        self.openImage(self.fname[0])


    def showDialog(self):
        return QFileDialog.getOpenFileName(parent = self, caption = "OpenFile" , filter ='Image Files (*.jpg *.png *.gif)' )

    def openImage(self, fileName):
        img = cv2.imread(fileName)
        self.cv2img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        assert not self.cv2img is None

        height, width, dim = self.cv2img.shape
        self.setFixedSize(width,height)

        loadedImage = QImage(self.cv2img.data, width, height, dim * width, QImage.Format_RGB888)
        newSize = loadedImage.size().expandedTo(self.size())
        self.resizeImage(loadedImage, newSize)
        self.image = loadedImage
        self.modified = False
        self.update()
        return True
    def cls(self):
        height, width, dim = self.cv2img.shape
        self.image = QImage(self.cv2img.data, width, height, dim * width, QImage.Format_RGB888)
        self.update()


    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            print("resizeImage:return")
            return

        newImage = QImage(newSize, QImage.Format_RGB32)
        newImage.fill(qRgb(255, 255, 255))
        painter = QPainter(newImage)
        painter.drawImage(QPoint(0, 0), image)
        self.image = newImage
        self.update()

        super(FreeTrim, self).resizeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rectData.newRect(event.pos())
            self.lastPoint = event.pos()
            self.scribbling = True
            self.rectData.updateRectByQPoint(event.pos())

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.scribbling:
            self.drawLineTo(event.pos())
            print(event.pos())
            print(event.pos().x(), event.pos().y())
            self.rectData.updateRectByQPoint(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.scribbling:
            self.drawLineTo(event.pos())
            self.scribbling = False
            self.rectData.updateRectByQPoint(event.pos())
            self.cls()
            self.drawAllRect()
            self.drawRectByFreeTrimRect(self.rectData.getCurrentRect())
            self.imgData.newImage(self.cv2img, self.rectData.getCurrentRect())

    def paintEvent(self, event):
        painter = QPainter(self)
        dirtyRect = event.rect()
        painter.drawImage(dirtyRect, self.image, dirtyRect)
        print('paint')

    def drawAllRect(self):
        for rect in self.rectData.getRects():
            self.drawRectByFreeTrimRect(rect)

    def drawRectByQRect(self, qrect):
        painter = QPainter(self.image)
        painter.setBrush(Qt.NoBrush)
        size = 3
        painter.setPen(QPen(Qt.red, size, Qt.SolidLine,
        Qt.RoundCap, Qt.RoundJoin))
        painter.drawRect(qrect)

        self.update(qrect.adjusted(-size, -size, +size, +size))

    def drawRectByFreeTrimRect(self,rect):
        self.drawRectByQRect(rect.getQRect())

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
