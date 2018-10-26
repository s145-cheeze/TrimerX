# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import  QApplication, QWidget, QLabel, QScrollArea, QVBoxLayout, QHBoxLayout, QDialog, QPushButton

from FreeTrimRect import *
from FreeTrimRectManager import *
from FreeTrimImage import *
from FreeTrimImageManager import *



class FreeTrimPreview(QDialog):
    """どのように切り取られるかを表示"""
    def __init__(self,fmanager ,  parent = None):
        super(FreeTrimPreview, self).__init__(parent)

        self.fmanager = fmanager

        #メイン画面
        self.setGeometry(300, 300, 1024, 768)
        self.scrollArea = QScrollArea()
        self.inner = QWidget()
        self.inner_layout = QVBoxLayout()
        self.inner.setLayout(self.inner_layout)
        self.labels = []

        #ラベルを貼る
        self.setLabels()

        #プレビュー画面
        self.scrollArea.setWidget(self.inner)
        self.base_layout = QHBoxLayout()

        #サイドのボタン
        self.side = QWidget()
        self.side_layout = QVBoxLayout()
        self.side.setLayout(self.side_layout)
        self.sideBtnOK = QPushButton('OK')
        self.sideBtnOK.clicked.connect(self.clicked_OK)
        self.sideBtnCancel = QPushButton('キャンセル')
        self.sideBtnCancel.clicked.connect(self.clicked_Cancel)
        self.side_layout.addWidget(self.sideBtnOK)
        self.side_layout.addWidget(self.sideBtnCancel)


        #上記２つをメイン画面に追加
        self.base_layout.addWidget(self.side)
        self.base_layout.addWidget(self.scrollArea)

        #名画面のレイアウトの設定
        self.setLayout(self.base_layout)

    def clicked_OK(self):
        self.fmanager.saveImages()
        self.close()

    def clicked_Cancel(self):
        self.close()

    def setLabels(self):
        for ft_file in self.fmanager.getFiles():
            self.labels.append(QLabel())
            s = f"<h1>{ft_file.getPath().stem}</h1>"
            self.labels[-1].setText(s)
            self.inner_layout.addWidget(self.labels[-1])
            for i, img in enumerate(ft_file.getImageManager().getImages()):
                img_name = str( "{}_{}{}".format(ft_file.getPath().stem, f"00{i}"[-2:], ft_file.getPath().suffix) )
                # ファイル名ラベル
                self.labels.append(QLabel())
                s = f"{i}:{img_name}"
                self.labels[-1].setText(s)
                self.inner_layout.addWidget(self.labels[-1])
                # 画像ラベル
                self.labels.append(QLabel())
                self.labels[-1].setPixmap(img.getQPixmap())
                self.inner_layout.addWidget(self.labels[-1])




def main():
    app = QApplication(sys.argv)
    ex1 = FreeTrimPreview(FreeTrimImageManager())
    ex1.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
