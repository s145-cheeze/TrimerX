# -*- coding: utf-8 -*-

from PyQt5.Qt import QRect

from FreeTrimRect import *

class FreeTrimRectManager(object):
    """切り取る範囲の矩形を管理する"""
    def __init__(self, pos = None):
        self.minX = None
        self.minY = None
        self.maxX = None
        self.maxY = None


        self.currentRect = None
        self.rects = []

        if pos != None:pass


    def getCurrentRect(self):
        """ 現在更新中の矩形返す """
        return self.currentRect

    def getRects(self):
        """ 全ての矩形データをジェネレーターで流す """
        for rect in self.rects:
            yield rect


    def pop(self):
        """ 一番後ろの矩形データを取り出す """
        return self.rects.pop()

    def hasAnyItems(self):
        """ リストの長さが0じゃないか """
        return len(self.rects) > 0

    def hasArea(self):
        """ 現在の矩形が面積を持っているか→辺の長さが0じゃないか """
        return self.minX != self.maxX and self.minY != self.maxY

    def updateRectByXY(self, x, y):
        """ 矩形を更新する """
        if self.currentRect is None:
            return
        self.minX = min(self.minX, x)
        self.minY = min(self.minY, y)
        self.maxX = max(self.maxX, x)
        self.maxY = max(self.maxY, y)
        self.currentRect.update(self.minX, self.minY, self.maxX, self.maxY)
        #print(self.currentRect)

    def updateRectByQPoint(self, pos):
        """ 矩形を更新する """
        self.updateRectByXY(pos.x(), pos.y())


    def newRect(self, pos):
        """ 新しい矩形を作る """
        self.minX = pos.x()
        self.minY = pos.y()
        self.maxX = pos.x()
        self.maxY = pos.y()

        self.currentRect = FreeTrimRect(self.minX, self.minY, self.maxX, self.maxY)
        self.rects.append(self.currentRect)