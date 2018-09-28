# -*- coding: utf-8 -*-

from PyQt5.QtCore import QPoint, QRect


class FreeTrimRect(object):
    """切り取る範囲の矩形のクラス"""
    def __init__(self, *args):
        super(FreeTrimRect, self).__init__()
        self.update(*args)
        self.img = None
    def get(self):
        return self.p1, self.p2
    def getQRect(self):
        return QRect(QPoint(*self.p1), QPoint(*self.p2))
    def update(self,*args):
        if len(args) == 4:
            self.p1 = args[0], args[1]
            self.p2 = args[2], args[3]
        elif len(args) == 2:
            self.p1 = args[0]
            self.p2 = args[1]
    def __repr__(self):
        return "FreeTrimRect<{},{}>".format(str(self.p1), str(self.p2))
