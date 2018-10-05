# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import cv2

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton, QFileDialog

from FreeTrimFile import *

class FreeTrimFileManager(object):
    """FreeTrimFileクラスを管理する"""
    def __init__(self, fnames = None):
        self.files_data = []
        self.current = None
        if fnames is None :
            return
        self.addFilesByDirPath(fnames)
    def addFileDilalog(self):
        fname, _ = self.showDialog()
        self.add(fname)
    def showDialog(self):
          return QFileDialog.getOpenFileName(parent = None, caption = "Open File" , filter ='Image Files (*.jpg *.png *.gif)' )
    def setCurrent(self, index):
        self.current = self.files_data[index]

    def getCurrent(self):
        if self.current == None:
            self.setCurrent(0)
        return self.current

    def isAddedRecently(self, path):
        """同じパスが入ってないか確認"""
        for fp in self.getFiles():
            if path.as_posix() == fp.getPath().as_posix():
                return True
        return False
    def add(self, fname):
        """ 追加 """
        path = fname if isinstance(fname, Path) else Path(fname).resolve()
        if not path.suffix in (".jpg", ".png" ,".gif"):
            return
        new_data = FreeTrimFile(path)
        self.files_data.append(new_data)

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
