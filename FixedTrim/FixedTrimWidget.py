# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import cv2

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import QFileDialog



from FixedTrim.FixedTrimRect import *
from FixedTrim.FixedTrimImage import *
from FixedTrim.FixedTrimImageManager import *



class FixedTrimWidget(QtWidgets.QWidget):
    """トリミングをする画面
    手順:
    1.画像読み込む
    2.読み込んだ画像が出てくる
    3.フリーハンドで切り取る
    4.フリーハンドの図形が矩形に変換される
    5.切り取った画像が表示される
    """
    def __init__(self,fmanager = None , fname = None, parent=None):
        super(FixedTrimWidget, self).__init__(parent)

        self.hbox = QtWidgets.QHBoxLayout(self)
        self.setLayout(self.hbox)

        self.setAttribute(Qt.WA_StaticContents)
        self.modified = False
        self.scribbling = False
        self.myPenWidth = 1
        self.myPenColor = Qt.blue
        self.image = QImage()
        self.lastPoint = QPoint()

        self.fmanager = fmanager
        self.changeImage()

    def changeImage(self, arg = None):
        """ トリミングする画像を変更する
        @param 変更したい画像．設定しない場合はFixedTrimFileManagerインスタンスで現在扱っているファイルに変更されます """
        if arg == None:
            self.rect_manager, self.img_manager = self.fmanager.getCurrent().getManagers()
        else :
            self.rect_manager, self.img_manager = arg.getCurrent().getManagers()
        self.image = self.img_manager.getMainQImage()
        height, width, dim = self.img_manager.getMainImage().shape
        self.setFixedSize(width,height)
        newSize = self.img_manager.getMainQImage().size().expandedTo(self.size())
        self.resizeImage(self.img_manager.getMainQImage(), newSize)
        self.drawAllRect()
        self.update()

        # self.rect_manager = FixedTrimRectManager()
        # self.img_manager = FixedTrimImageManager()
    def setFile(self, fname = None):
        """ 読み込むファイルを設定します
        @param fname 読み込みたいファイル名．省略した場合は「ファイルを開く」ダイアログがでます """
        if fname == None:
            self.fname, _ = self.showDialog()
            print(f"fname:{self.fname}")
        else:
            self.fname = fname
        self.openImage(self.fname)


    def showDialog(self):
        """ 「ファイルを開く」ダイアログを呼びます """
        return QFileDialog.getOpenFileName(parent = self, caption = "Open File" , filter ='Image Files (*.jpg *.png *.gif)' )

    def openImage(self, fname):
        """ 画像ファイルを開きます
        @param fname 読み込む画像ファイルの名前 """
        img = cv2.imread(fname)
        assert not img is None
        self.cv2img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        height, width, dim = self.cv2img.shape
        self.setFixedSize(width,height)

        # print("self.cv2img:")
        # print(self.cv2img)
        # print("type(self.cv2img):")
        # print(type(self.cv2img))
        # print("self.cv2img.data:")
        # print(self.cv2img.data)
        # print("type(self.cv2img.data):")
        # print(type(self.cv2img.data))

        loadedImage = QImage(self.cv2img.data, width, height, dim * width, QImage.Format_RGB888)
        newSize = loadedImage.size().expandedTo(self.size())
        self.resizeImage(loadedImage, newSize)
        self.image = loadedImage
        self.modified = False
        self.update()
        return True
    def cls(self):
        """ 表示画面を初期化します """
        self.image = self.img_manager.getMainQImage()
        self.update()


    def resizeImage(self, image, newSize):
        """ 画像ファイルのサイズを変更する
        @param image 画像ファイル
        @param newSize 新しいサイズ """
        if image.size() == newSize:
            print("resizeImage:return")
            return

        newImage = QImage(newSize, QImage.Format_RGB32)
        newImage.fill(qRgb(255, 255, 255))
        painter = QPainter(newImage)
        painter.drawImage(QPoint(0, 0), image)
        self.image = newImage
        self.update()

        super(FixedTrim, self).resizeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rect_manager.newRect(event.pos())
            self.lastPoint = event.pos()
            self.scribbling = True
            self.rect_manager.updateRectByQPoint(event.pos())

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.scribbling:
            self.drawLineTo(event.pos())
            #print(event.pos())
            #print(event.pos().x(), event.pos().y())
            self.rect_manager.updateRectByQPoint(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.scribbling:
            self.drawLineTo(event.pos())
            self.scribbling = False
            self.rect_manager.updateRectByQPoint(event.pos())
            self.cls()
            self.drawAllRect()
            if not self.rect_manager.hasArea():
                self.rect_manager.pop()
                self.cls()
                self.drawAllRect()
                return
            img = self.img_manager.newImage( self.rect_manager.getCurrentRect())
            #cv2.imshow(f"img:{self.rect_manager.getCurrentRect()}", img.get()[:,:,::-1])

    def paintEvent(self, event):
        painter = QPainter(self)
        dirtyRect = event.rect()
        painter.drawImage(dirtyRect, self.image, dirtyRect)
        #print('paint')

    def drawAllRect(self):
        """ 現在扱っているファイルの矩形データを全て描画する """
        for rect in self.rect_manager.getRects():
            self.drawRectByFixedTrimRect(rect)

    def drawRectByQRect(self, qrect):
        """ 矩形を描画する
        @param 描画する矩形(QRectクラス) """
        painter = QPainter(self.image)
        painter.setBrush(Qt.NoBrush)
        size = 3
        painter.setPen(QPen(Qt.red, size, Qt.SolidLine,
        Qt.RoundCap, Qt.RoundJoin))
        painter.drawRect(qrect)

        self.update(qrect.adjusted(-size, -size, +size, +size))

    def drawRectByFixedTrimRect(self,rect):
        """ 矩形を描画する
        @param 描画する矩形(FixedTrimRectクラス) """
        self.drawRectByQRect(rect.getQRect())

    def drawLineTo(self, endPoint):
        """ 線を描画する
        @param endPoint 引きたい線の終点 """
        painter = QPainter(self.image)
        painter.setPen(QPen(self.myPenColor, self.myPenWidth, Qt.SolidLine,
        Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.lastPoint, endPoint)
        self.modified = True

        rad = self.myPenWidth / 2 + 2
        self.update(QRect(self.lastPoint, endPoint).normalized().adjusted(-rad, -rad, +rad, +rad))
        self.lastPoint = QPoint(endPoint)

def main():
    app = QApplication(sys.argv)
    ex1 = FixedTrimWidget()
    ex1.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
