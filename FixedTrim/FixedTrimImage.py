# -*- coding: utf-8 -*-

import cv2
import numpy as np

from PyQt5.QtGui import QImage, QPixmap

class FixedTrimImage(object):
    """トリミングした画像のデータと矩形データ"""
    def __init__(self,img,rect):
        super(FixedTrimImage, self).__init__()
        self.rect = rect
        p1 , p2 = rect.get()
        self.img = img[p1[1]:p2[1],p1[0]:p2[0],:]
    def get(self):
        """ このインスタンスが持っている画像を返します """
        return self.img
    #これ同じ操作じゃね？→コメントアウト
    # def create_QPixmap(self):
    #     img = self.img.copy()
    #     qimage = QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * img.shape[2], QImage.Format_RGB888)
    #     pixmap = QPixmap.fromImage(qimage)
    #     return pixmap
    def getQImage(self):
        """ このインスタンスが持っている画像をQImageクラスに変換して返します """
        # OpenCVの画像データをQImageに変換
        img = self.img.copy()
        return QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * img.shape[2], QImage.Format_RGB888)
    def getQPixmap(self):
        """ このインスタンスが持っている画像をQPixmapクラスに変換して返します """
        #QImageをQPixmapに変換し、アイテムとして読み込む
        return QPixmap.fromImage(self.getQImage())
