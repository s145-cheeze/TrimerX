# -*- coding: utf-8 -*-

from FreeTrimRect import *

class FreeTrimRectData(object):
    """切り取る範囲の矩形をまとめるクラス"""
    def __init__(self):
        self.minX = None
        self.minY = None
        self.maxX = None
        self.maxY = None

        self.currentRect = None
        self.rects = []

    def getCurrentRect(self):
        return self.currentRect

    def getRects(self):
        for rect in self.rects:
            yield rect


    def pop(self):
        return self.rects.pop()

    def hasAnyItems(self):
        return len(self.rects) > 0

    def hasArea(self):
        return self.minX!=self.maxX and self.minY != self.maxY

    def updateRectByXY(self, x, y):
        if self.currentRect is None:
            return
        self.minX = min(self.minX, x)
        self.minY = min(self.minY, y)
        self.maxX = max(self.maxX, x)
        self.maxY = max(self.maxY, y)
        self.currentRect.update(self.minX, self.minY, self.maxX, self.maxY)
        #print(self.currentRect)

    def updateRectByQPoint(self, pos):
        self.updateRectByXY(pos.x(), pos.y())


    def newRect(self, pos):
        self.minX = pos.x()
        self.minY = pos.y()
        self.maxX = pos.x()
        self.maxY = pos.y()

        self.currentRect = FreeTrimRect(self.minX, self.minY, self.maxX, self.maxY)
        self.rects.append(self.currentRect)
