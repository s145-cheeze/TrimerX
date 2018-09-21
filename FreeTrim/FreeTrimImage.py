# -*- coding: utf-8 -*-

import cv2
import numpy as np

from PyQt5.QtGui import QImage, QPixmap

class FreeTrimImage(object):
    """docstring for FreeTrimImage."""
    def __init__(self,img,rect):
        super(FreeTrimImage, self).__init__()
        self.rect = rect
        p1 , p2 = rect.get()
        self.img = img[p1[1]:p2[1],p1[0]:p2[0],:]
    def get(self):
        return self.img
    def create_QPixmap(self):
        qimage = QImage(self.img.data, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        return pixmap
    def getQImage(self):
        height, width, dim = self.img.shape
        return QImage(self.img.data, width, height, dim * width, QImage.Format_RGB888)
    def getQPixmap(self):
        #QImageをQPixmapに変換し、アイテムとして読み込む
        return QPixmap.fromImage(self.getQImage())
