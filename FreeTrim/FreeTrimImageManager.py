# -*- coding: utf-8 -*-

from pathlib import Path

import cv2

from FreeTrim.FreeTrimImage import *


class FreeTrimImageManager(object):
    """トリミングした画像をまとめるクラス"""
    def __init__(self, path):
        super(FreeTrimImageManager, self).__init__()
        self.main_img = cv2.imread(path.as_posix())[:,:,::-1]
        self.sub_imgs = []
    def getMainImage(self):
        return self.main_img.copy()
    def getMainQImage(self):
        img = self.main_img.copy()
        return QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * img.shape[2], QImage.Format_RGB888)
    def getImage(self, index):
        if len(self.sub_imgs) == 0 :return None
        if abs(index) < len(self.sub_imgs) or index == -len(self.sub_imgs):
            return self.sub_imgs[index]
        return None
    def getLength(self):
        return len(self.sub_imgs)
    def getImages(self):
        for img in self.sub_imgs:
            yield img
    def newImage(self, rect):
        img = FreeTrimImage(self.main_img, rect)
        self.sub_imgs.append(img)
        return img
    def pop(self):
        return self.sub_imgs.pop()
