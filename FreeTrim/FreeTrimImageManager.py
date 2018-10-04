# -*- coding: utf-8 -*-

from FreeTrimImage import *


class FreeTrimImageManager(object):
    """トリミングした画像をまとめるクラス"""
    def __init__(self):
        super(FreeTrimImageManager, self).__init__()
        self.imgs = []
    def getImages(self):
        for img in self.imgs:
            yield img
    def newImage(self, img, rect):
        img = FreeTrimImage(img, rect)
        self.imgs.append(img)
        return img
    def pop(self):
        return self.imgs.pop()
