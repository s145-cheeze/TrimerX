# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import cv2

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton

# NOTE:使わないかも
class FreeTrimFilePathData(object):
    """ファイルの情報をまとめる"""
    def __init__(self, path, img):
        self.parent_path = path if isinstance(path, Path) else Path(path).resolve()
        # self.child_paths = []
    def getPath(self):
        return parent_path
    def getPathString(self):
        return str(parent_path)
    def getFileName(self):
        return str(parent_path.stem)
    # def getPathByIndex(self, index):
    #     return child_paths[index]
    # def getPathStringByIndex(self, index):
    #     return str(child_paths[index])
    # def getFileNameByIndex(self, index):
    #     return str(child_paths[index].stem)
    # def getPaths(self):
    #     for child_path in self.child_paths:
    #         yield child_path
    # def getPathStrings(self):
    #     for child_path in self.child_paths:
    #         yield str(child_path)
    def getFileNames(self):
        for child_path in self.child_paths:
            yield str(child_path.stem)
    def append(self, path):
        child_path = path if isinstance(path, Path) else Path(path).resolve()
        self.child_paths.append(child_path)
    def pop(self):
        return self.child_paths.pop()
