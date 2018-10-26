# -*- coding: utf-8 -*-

import sys
import csv
import datetime
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
        self.fname = None
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
    def getDataLists(self):
        for file_data in self.files_data:
            yield file_data.getDataList()

    def get(self, index):
        """ インデックスを指定して取得 """
        return self.files_data[index]
    def saveImages(self, dname = None):
        """ ディレクトリを指定して保存 """
        dir_name = QFileDialog.getExistingDirectory(self) if dname is None else dname
        if len(dir_name) == 0:
            return
        print(dir_name)

        for ft_file in self.getFiles():
            # NOTE:ここのごちゃごちゃなんとかならない？
            for i, img in enumerate(ft_file.getImageManager().getImages()):
                img_name = str(Path(dir_name, "{}_{}{}".format(ft_file.getPath().stem, f"00{i}"[-2:], ft_file.getPath().suffix) ))
                print(img_name)
                cv2.imwrite(img_name, img.get()[:,:,::-1])
    def saveFile(self, isMakeNewFile = False):
        if self.fname is None or isMakeNewFile:
            self.fname, _ = QFileDialog.getSaveFileName(parent = None, caption = "Save File" , filter ='Free Trim Data (*.ftd)',
                directory = './FreeTrimData({}).ftd'.format(
                        datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                    )
                )
        if self.fname == '':
            return -1
        path = Path(self.fname)
        with open(path,"w") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(list(self.getDataLists()))
            print("saved datas:")
            print(*list(self.getDataLists()) , sep='\n')


    def importDataList(self, dlist):
        new_data = FreeTrimFile.fromDataList(*dlist)
        if new_data == -1:
            return -1
        if self.isAddedRecently(new_data.getPath()):
            return 0
        self.files_data.append(new_data)
    #
    #
    #
    # def importDataLists(self, dlists):
    #     for dlist in dlists:
    #         self.importDataList(dlist)
    #
    # def importFile(self, fname = None):
    #     if self.fname is None and fname is None:
    #         self.fname = FreeTrimFileManager.getOpenDataFileDilalog()
    #     if self.fname == '':
    #         return -1
    #     path = Path(fname)


    @staticmethod
    def getOpenDataFileDilalog():
        return QFileDialog.getOpenFileName(parent = None, caption = "Open File" , filter ='Free Trim Data (*.ftd)' )[0]
    @staticmethod
    def fromFile(fname = None):
        """ファイルからインスタンスを設定"""
        if fname is None:
            fname = FreeTrimFileManager.getOpenDataFileDilalog()
        if fname == '':
            return -1
        path = Path(fname)
        ret = FreeTrimFileManager()
        with open(path,"r") as f:
            reader = csv.reader(f)
            print("read datas:")
            for row in reader:
                ret.importDataList(row)
        return ret
