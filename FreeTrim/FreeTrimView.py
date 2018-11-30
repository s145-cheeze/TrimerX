# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import  QApplication, QWidget, QLabel, QScrollArea, QVBoxLayout, QHBoxLayout, QDialog, QPushButton, QListWidget

from FreeTrim.FreeTrimRect import *
from FreeTrim.FreeTrimRectManager import *
from FreeTrim.FreeTrimImage import *
from FreeTrim.FreeTrimImageManager import *
from FreeTrim.FreeTrimFileManager import *


class FreeTrimView(QWidget):
    """ 切り取ったやつを表示 """
    # セットアップ-------------------------------------------------------------------
    def __init__(self, fmanager = None,  parent = None):
        super(FreeTrimView, self).__init__(parent)

        self.fmanager = fmanager if fmanager is not None else FreeTrimFileManager.fromFile(ft_widget = self)

        #メイン画面
        self.setGeometry(300, 300, 1024, 768)
        self.scrollArea = QScrollArea()
        self.inner = QWidget()
        self.inner_layout = QVBoxLayout()
        self.inner.setLayout(self.inner_layout)
        self.labels = []

        #ラベルを貼る
        self.initLabels()

        #プレビュー画面
        self.scrollArea.setWidget(self.inner)
        self.base_layout = QHBoxLayout()

        #サイドのボタン
        self.side = QWidget()
        self.side_layout = QVBoxLayout()
        self.side.setLayout(self.side_layout)
        self.sideBtnOK = QPushButton('全ての画像を保存')
        self.sideBtnOK.clicked.connect(self.clicked_OK)
        self.sideBtnCancel = QPushButton('終了')
        self.sideBtnCancel.clicked.connect(self.clicked_Cancel)
        self.side_layout.addWidget(self.sideBtnOK)
        self.side_layout.addWidget(self.sideBtnCancel)

        self.setListBox()


        #上記２つをメイン画面に追加
        self.base_layout.addWidget(self.side)
        self.base_layout.addWidget(self.scrollArea)

        #メイン画面のレイアウトの設定
        self.setLayout(self.base_layout)

    def initLabels(self):
        self.maxLength = self.fmanager.getGeneratorMax()
        for i in range(self.maxLength):
            # ファイル名ラベル
            self.labels.append(QLabel(f"{i}"))
            self.inner_layout.addWidget(self.labels[-1])
            # 画像ラベル
            self.labels.append(QLabel())
            self.inner_layout.addWidget(self.labels[-1])

    def clicked_OK(self):
        self.fmanager.saveImages()
        self.close()

    def clicked_Cancel(self):
        self.close()
    def setListBox(self):
        self.list_widget = QListWidget()

        for i in range(self.fmanager.getMaxLength()):
            self.list_widget.addItem(f"{i+1}")

        #選択行が変わったらイベン
        self.list_widget.currentRowChanged.connect(self.listMove)
        self.side_layout.addWidget(self.list_widget)
    def listMove(self, index):
        print(index)
        self.setLabels(index)
    def setLabels(self,index):
        for label in self.labels:
            label.clear()
        for i, p in enumerate(self.fmanager.getImagesUsingIndex(index)):
            img, ft_id, ft_file = p
            img_name = str( "{}_{}{}".format(ft_file.getPath().stem, f"00{i}"[-2:], ft_file.getPath().suffix) )
            print(img_name)
            # ファイル名ラベル
            s = str(f"{i}:{img_name}")
            self.labels[2*i].setText(s)
            # 画像ラベル
            self.labels[2*i+1].setPixmap(img.getQPixmap())
            self.labels[2*i+1].setMinimumSize(img.getQPixmap().size())





def main():
    app = QApplication(sys.argv)
    ex1 = FreeTrimPreview(FreeTrimImageManager())
    ex1.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
