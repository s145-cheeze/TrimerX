# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import cv2

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton

from FreeTrimImageManager import *
from FreeTrimRectManager import *

class FreeTrimFile(object):
    """ファイルの情報をまとめる"""
    def __init__(self, path):
        # ファイルの場所，名前→
        self.path = path if isinstance(path, Path) else Path(path).resolve()
        # 切り取る領域を保存するとこ
        self.rect_manager = FreeTrimRectManager()
        self.img_manager = FreeTrimImageManager(self.path)
    def getRectManager(self):
        return self.rect_manager
    def getImageManager(self):
        return self.img_manager
    def getManagers(self):
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
