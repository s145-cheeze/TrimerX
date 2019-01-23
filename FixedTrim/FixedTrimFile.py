# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import cv2

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton

from FixedTrim.FixedTrimImageManager import *
#from FreeTrim.FreeTrimRectManager import *

class FixedTrimFile(object):
    """ファイルの情報をまとめる"""
    def __init__(self, path):
        # ファイルの場所，名前→
        self.path = path if isinstance(path, Path) else Path(path).resolve()
        # 切り取る領域を保存するとこ
        # self.rect_manager = FixedTrimRectManager()
        # 切り取った画像を保存しているところ
        self.img_manager = FixedTrimImageManager(self.path)
    def getRectManager(self):
        """ このインスタンスが持っているFixedTrimRectManagerインスタンスを取得 """
        return self.rect_manager
    def getImageManager(self):
        """ このインスタンスが持っているFixedTrimImageManagerインスタンスを取得 """
        return self.img_manager
    def getManagers(self):
        """ このインスタンスが持っているFixedTrimRectManager, FixedTrimImageManagerインスタンスの両方を取得 """
        return self.getRectManager(), self.getImageManager()
    def getPath(self):
        """ ファイルのパス返す """
        return self.path
    def getPathString(self):
        """ ファイルのパスを文字列で返す """
        return str(self.path)
    def getFileName(self):
        """ ファイル名を返す """
        return self.path.stem
    def getRectsManager(self):
        """ 矩形をまとめるクラスを返す """
        return self.rect_manager

    def getDataList(self):
        """ データをリストにして返す """
        lst = [self.getPathString()]
        lst.extend([ i for i in self.rect_manager.getRectsForDatalist()])
        return lst
    @staticmethod
    def fromDataList(*data_lst):
        """ データリストからインスタンスを生成 """
        if len(data_lst) % 4 != 1:
            return -1
        tmp_lst = list(range(4))
        ret = FixedTrimFile(data_lst[0])
        rect_manager, img_manager = ret.getManagers()
        rect_list = []

        for cnt, data in enumerate(data_lst[1:]):
            i = cnt % 4
            tmp_lst[i] = int(data)
            if i != 3 : continue
            tmp_rect = rect_manager.addRect( *tmp_lst )
            img_manager.newImage( tmp_rect )
        return ret
