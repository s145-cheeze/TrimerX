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

    def mousePressEvent(self, event: Qg.QMouseEvent):
        self.onMousePress.emit(event)
        print("press")

    def mouseMoveEvent(self, event: Qg.QMouseEvent):
        self.onMouseMove.emit(event)
        print("move")

    def mouseReleaseEvent(self, event: Qg.QMouseEvent):
        self.onMouseRelease.emit(event)
        print("release")

    def mouseDoubleClickEvent(self, event: Qg.QMouseEvent):
        self.onDoubleClick.emit(event)
