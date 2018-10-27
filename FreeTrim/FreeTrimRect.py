# -*- coding: utf-8 -*-

from PyQt5.QtCore import QPoint, QRect


class FreeTrimRect(object):
    """切り取る範囲の矩形のクラス"""
    def __init__(self, *args):
        super(FreeTrimRect, self).__init__()
        self.update(*args)
        self.img = None
    def get(self):
        """ このインスタンスが持っている矩形の座標を返します """
        return self.p1, self.p2
    def getQRect(self):
        """ このインスタンスが持っている矩形の座標をQRect型で返します """
        return QRect(QPoint(*self.p1), QPoint(*self.p2))
    def update(self,*args):
        """ このインスタンスが持っている矩形データを更新します
        @param args 矩形情報
        矩形情報の解釈の仕方は以下の通りです
        argの大きさが2の時:
            arg[0] 左上座標
            arg[1] 右下座標
        argの大きさが4の時:
            arg[0] 左上X座標
            arg[1] 左上Y座標
            arg[2] 右下X座標
            arg[3] 右下Y座標 """
        if len(args) == 4:
            self.p1 = args[0], args[1]
            self.p2 = args[2], args[3]
        elif len(args) == 2:
            self.p1 = args[0]
            self.p2 = args[1]
    def __repr__(self):
        return "FreeTrimRect<{},{}>".format(str(self.p1), str(self.p2))
