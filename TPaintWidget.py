# -*- coding: utf-8 -*-
from PyQt5 import QtCore as Qc, QtGui as Qg, QtWidgets as Qw

#http://www7a.biglobe.ne.jp/~thor/novel/column/07.html

#QObjectを継承しなければいけない（QWidgetは大丈夫）
class TPaintWidget(Qw.QWidget):

    #シグナル定義。パラメータの「型」を引数にする
    onPaint = Qc.pyqtSignal(Qg.QPaintEvent, Qg.QPainter)
    onMousePress = Qc.pyqtSignal(Qg.QMouseEvent)
    onMouseMove = Qc.pyqtSignal(Qg.QMouseEvent)
    onMouseRelease = Qc.pyqtSignal(Qg.QMouseEvent)
    onDoubleClick = Qc.pyqtSignal(Qg.QMouseEvent)

    def paintEvent(self, event: Qg.QPaintEvent):
        canvas = Qg.QPainter(self)
        self.onPaint.emit(event, canvas)                #シグナルの発行
        print("paint")
        print(dir(event))

    def mousePressEvent(self, event: Qg.QMouseEvent):
        self.onMousePress.emit(event)
        print("press")
        print(dir(event))

    def mouseMoveEvent(self, event: Qg.QMouseEvent):
        self.onMouseMove.emit(event)
        print("move")
        print(dir(event))

    def mouseReleaseEvent(self, event: Qg.QMouseEvent):
        self.onMouseRelease.emit(event)
        print("release")
        print(dir(event))

    def mouseDoubleClickEvent(self, event: Qg.QMouseEvent):
        self.onDoubleClick.emit(event)
        print(dir(event))
