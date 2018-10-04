# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import cv2

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton

from FreeTrimFile import *

class FreeTrimFileManager(object):
    """FreeTrimFileクラスを管理する"""
    def __init__(self, fnames = None):
        self.files_data = []
        if fnames is None :return
        for fname in fnames:
            file_data = FreeTrimFile(fname)
            self.files_data.append(file_data)

    def isAddedRecently(self, path):
        """同じパスが入ってないか確認"""
        for fp in self.getFileName():
            if path.as_posix == fp.as_posix:
                return True
        return False
    def add(self, fname):
        """ 追加 """
        new_data = FreeTrimFile(fname)
        self.files_data.append(file_data)

    def addFilesByDirPath(self, dir_path):
        """ ディレクトリのパスからまとめて取得する """
        if not dir_path.is_dir():
            return
        for path in dir_path.glob("*"):
            # print(path.stem)
            #拡張子の確認
            if not path.suffix in (".jpg", ".png" ,".gif"):
                continue
            if self.isAddedRecently(path):
                continue
            new_data = FreeTrimFile(path)
            self.files_data.append(new_data)


    def getFiles(self):
        """ 全部取得 """
        for file_data in self.files_data:
            yield file_data
    def get(self, index):
        """ インデックスを指定して取得 """
        return self.files_data[index]
