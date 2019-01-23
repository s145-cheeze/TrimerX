# -*- coding: utf-8 -*-

import cv2
import numpy as np
from pathlib import Path

from PyQt5.QtGui import QImage, QPixmap

class Images(object):
    def __init__(self):
        self.imgs = []
    def getLength(self):
        return len(self.imgs)
    def getImages(self):
        for img in self.imgs:
            yield img
    def getImage(self, index):
        if len(self.imgs) == 0 :return None
        if abs(index) < len(self.imgs) or index == -len(self.imgs):
            return self.imgs[index]
        return None
    def hasAnyItems(self):
        return len(self.imgs) > 0
    def isAddedRecently(self, path):
        """ 同じパスが入ってないか確認
        @return 同じパスが入っていたらTrue,でなければFalse """
        if not isinstance(path, Path):
            return False
        for fp in self.imgs:
            if path.as_posix() == fp.getPath().as_posix():
                return True
        return False
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
            new_data = Image(path)
        except TypeError as e:
            print(e)
            return False
        self.imgs.append(new_data)
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
    def newImage(self, imgpath):
        img = Image(imgpath)
        self.imgs.append(img)
        return img


class Image(object):
    def __init__(self, imgpath):
        self.imgpath = imgpath if isinstance(imgpath, Path) else Path(imgpath).resolve()
        self.img = cv2.imread(imgpath.as_posix())[:,:,::-1]
    def __len__(self):
        return len(self.rects)
    def get(self):
        return self.img
    def getPath(self):
        return self.imgpath
    def getQImage(self):
        img = self.img.copy()
        return QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * img.shape[2], QImage.Format_RGB888)
    def getQPixmap(self):
        return QPixmap.fromImage(self.getQImage())
