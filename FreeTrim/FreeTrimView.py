# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import  QApplication, QWidget, QLabel, QScrollArea, QFormLayout, QVBoxLayout, QHBoxLayout, QDialog, QPushButton, QListWidget, QStackedWidget

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
        self.inner = QStackedWidget()
        self.sub_inner = FTViewSubWidget(self.inner,self.fmanager,0)
        self.inner.addWidget(self.sub_inner)
        self.inner.setCurrentWidget(self.sub_inner)
        self.sub_widgets = []
        self.labels = []

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
        #print(index)
        self.setLabels(index)
    def setLabels(self,index):
        tmp = self.sub_inner
        self.sub_inner = FTViewSubWidget(self, self.fmanager, index)
        self.inner.addWidget(self.sub_inner)
        self.inner.setCurrentWidget(self.sub_inner)
        self.inner.removeWidget(tmp)

class FTViewSubWidget(QWidget):
    def __init__(self, parent, fmanager, index):
        super(FTViewSubWidget, self).__init__(parent)
        self.sub_widgets = []
        box = QVBoxLayout()
        self.setLayout(box)
        for i, p in enumerate(fmanager.getImagesUsingIndex(index)):
            img, ft_id, ft_file = p
            sub_widget = FTViewSubSubWidget(self)
            self.sub_widgets.append(sub_widget)
            img_name = str( "{}_{}{}".format(ft_file.getPath().stem, f"00{i}"[-2:], ft_file.getPath().suffix) )
            # ファイル名ラベル
            s = f"{i+1}:{img_name}"
            sub_widget.setImg(s, img)
            box.addWidget(sub_widget)


class FTViewSubSubWidget(QWidget):
    def __init__(self, parent = None):
        super(FTViewSubSubWidget, self).__init__(parent)
        self.name          = QLabel()
        self.img_widget    = QWidget()
        self.img           = QLabel(self.img_widget)
        self.layout        = QVBoxLayout()
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.img)
        self.setLayout(self.layout)
    def setImg(self, name, img):
        self.resize(img.getQPixmap().size())
        self.name.setText(name)
        self.img.setPixmap(img.getQPixmap())
        self.img.resize(img.getQPixmap().size())
        self.img_widget.resize(img.getQPixmap().size())
    def cls(self):
        self.name.clear()
        self.img.clear()






def main():
    app = QApplication(sys.argv)
    ex1 = FreeTrimPreview(FreeTrimImageManager())
    ex1.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
