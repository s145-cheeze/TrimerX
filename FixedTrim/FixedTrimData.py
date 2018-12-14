# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import cv2

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton

class FixedTrimData(object):
    """トリミングの情報とか色々まとめる,csv出力もする"""
    def __init__(self):
        self.paths = ""
    def addPath(self, path):
        new_path = path if isinstance(path, Path) else Path(path)
        self.paths.append(new_path)
    def getPaths(self):
        for path in self.paths:
            yield path
    def getPathByIndex(self, index):
        return self.paths[index]
