# -*- coding: utf-8 -*-

import sys
import csv
import datetime
from pathlib import Path
import pickle

import cv2

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton, QFileDialog

from FreeTrim.FreeTrimFile import *

class FreeTrimFileManager(object):
    """FreeTrimFileクラスを管理する"""
    def __init__(self, fnames = None):
        self.fname = None
        self.files_data = []
        self.current = None
        if fnames is None :
            return
        self.addFilesByDirPath(fnames)
    def addFileDilalog(self, ft_widget = None):
        fname, _ = self.showDialog(ft_widget)
        self.add(fname)
    def showDialog(self, ft_widget = None):
        return QFileDialog.getOpenFileName(parent = ft_widget, caption = "Open File" , filter ='Image Files (*.jpg *.png *.gif)' )
    # getter/setter------------------------------------------------------------
    def setCurrent(self, index):
        """ FreeTrimFileインスタンスを選択
        @param index 選択するFreeTrimFileインスタンスの番号 """
        self.current = self.files_data[index]

    def getCurrent(self):
        """ 選択中のFreeTrimFileインスタンスを取得
        @return 選択中のFreeTrimFileインスタンス """
        if self.current == None:
            self.setCurrent(0)
        return self.current
    def getMaxLength(self):
        """ 切り取り画像を集めているリストの長さの中で最長はいくつかを返す
        @return 大きい切り取り画像リストの長さ"""
        return max([ft_file.getImageManager().getLength() for ft_file in self.getFiles()])

    def getGeneratorMax(self):
        """ getImagesUsingIndexで返されるジェネレータの大きさの最大を返す
        @return 大きい切り取り画像リストの長さ"""
        length = self.getMaxLength()
        return max([ self.getImagesUsingIndexLength(i) for i in range(length)])

    def getImagesUsingIndex(self, index):
        """ インデックスを指定してその番号の画像を全てのFreeTrimFileインスタンスから取得するジェネレーターを返す
        @param 取得する画像群のインデックス
        @yield タプル:(画像データ, 画像id, 切り取り元ファイル)"""
        for i, file_data in enumerate(self.getFiles()):
            img_manager = file_data.getImageManager()
            img = img_manager.getImage(index)
            if img is not None:
                yield img, i, file_data
    def getImagesUsingIndexLength(self, index):
        """ getImagesUsingIndexLengthが生成するジェネレーターの大きさを返す
        @param 取得する画像群のインデックス
        @return ジェネレーターの大きさ"""
        cnt = 0
        for i, file_data in enumerate(self.getFiles()):
            img_manager = file_data.getImageManager()
            img = img_manager.getImage(index)
            if img is not None:
                cnt += 1
        return cnt
    def get(self, index):
        """ インデックスを指定して取得 """
        return self.files_data[index]
    def getFiles(self):
        """ 全部取得 """
        for file_data in self.files_data:
            yield file_data
    def getDataLists(self):
        for file_data in self.files_data:
            yield file_data.getDataList()
    # チェック用関数------------------------------------------------------------------
    def isAddedRecently(self, path):
        """ 同じパスが入ってないか確認
        @return 同じパスが入っていたらTrue,でなければFalse """
        if not isinstance(path, Path):
            return False
        for fp in self.getFiles():
            if path.as_posix() == fp.getPath().as_posix():
                return True
        return False
    def hasAnyItems(self):
        return len(self.files_data) > 0
    #追加用関数---------------------------------------------------------------------
    def add(self, fname):
        """ ファイル追加
        @param fname 追加したいファイル名またはPath
        @return 追加できたらTrueできなかったらFalse """
        path = fname if isinstance(fname, Path) else Path(fname).resolve()
        #拡張子の確認
        if not path.suffix in (".jpg", ".png" ,".gif", ".JPG", ".PNG" ,".GIF"):
            return False
        if self.isAddedRecently(path):
            return False
        try:
            new_data = FreeTrimFile(path)
        except TypeError as e:
            print(e)
            return False
        self.files_data.append(new_data)
        return True

    def addFilesByDirPath(self, dir_path):
        """ ディレクトリのパスからまとめて取得する
        @param dir_path 取得するディレクトリのパス
        @return dir_pathがディレクトリのパスではないと-2,何も追加できなかったら-1,追加できたら追加できたファイルの個数を返します．"""
        if not dir_path.is_dir():
            return -2
        cnt = 0
        for path in dir_path.glob("*"):
            # print(path.stem)
            if self.add(path):
                cnt += 1
        return cnt if cnt > 0 else -1
    #ファイル関係--------------------------------------------------------------------
    def ImageName(self, ft_file, index):
        """ 切り取り画像のファイル名生成
        @param index 生成したい番号
        @para, ft_file 生成したいファイル名の元ファイル"""
        fstem  = ft_file.getPath().stem
        number = f"{index:02d}"
        ext    = ft_file.getPath().suffix
        img_name  = f"{fstem}_{number}{ext}"
        return img_name
    def saveImages(self, dname = None, ft_widget = None):
        """ ディレクトリを指定して保存 """
        dir_name = QFileDialog.getExistingDirectory(parent = ft_widget) if dname is None else dname
        if len(dir_name) == 0:
            return
        print(dir_name)

        for ft_file in self.getFiles():
            for i, img in enumerate(ft_file.getImageManager().getImages()):
                fstem  = ft_file.getPath().stem
                number = f"00{i}"[-2:]
                ext    = ft_file.getPath().suffix
                fpath  = "{}_{}{}".format(fstem, number, ext )
                img_name = str(Path(dir_name, fpath))
                print(img_name)
                cv2.imwrite(img_name, img.get()[:,:,::-1])
    def saveFile(self, isMakeNewFile = False, FTparent = None):
        if self.fname is None or isMakeNewFile:
            self.fname, _ = QFileDialog.getSaveFileName(parent = FTparent, caption = "Save File" , filter ='Free Trim Data (*.ftd)',
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
    @staticmethod
    def getOpenDataFileDilalog(ft_widget = None):
        return QFileDialog.getOpenFileName(parent = ft_widget, caption = "Open File" , filter ='Free Trim Data (*.ftd)' )[0]
    @staticmethod
    def fromFile(fname = None, ft_widget = None):
        """ファイルからインスタンスを設定"""
        if fname is None:
            fname = FreeTrimFileManager.getOpenDataFileDilalog(ft_widget)
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
    def saveFile_(self):
        fname, _ = QFileDialog.getSaveFileName(parent = None, caption = "Save File" , filter ='Free Trim Data Serialized (*.ftds)',
            directory = './TrimerXAnswerCheckData({}).txacd'.format(
                    datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                )
            )
        with open(fname,"wb") as f:
            pickle.dump(self, f)
    @staticmethod
    def loadFile_(fname = None):
        if fname is None:
            fname , _ =QFileDialog.getOpenFileName(parent = None, caption = "Open File" , filter ='Free Trim Data Serialized (*.ftds)')
        if fname == '':
            return -1
        with open(fname,"rb") as f:
            return pickle.load(f, encoding="ASCII")
