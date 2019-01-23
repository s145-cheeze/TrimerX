# -*- coding: utf-8 -*-

import sys
from pathlib import Path
from enum import Enum, auto

import cv2

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QImage, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget, QFileDialog, QLabel

from AnsChk.Images import *



class ACILS_Result(Enum):
    """ AnsChkMainクラスにOKかキャンセルかを伝える列挙型
    ACILS = AnsChkImportListSettingの単語の頭文字
    """
    OK = auto()
    Cancel = auto()


class AnsChkImportListSetting(QWidget):
    """トリミングしたい画像を指定する"""
    def __init__(self,imgs ,parent = None):
        super(AnsChkImportListSetting, self).__init__(parent)
        self.outer = None
        self.index = -1
        self.imgs = imgs
        self.initUI()
    def connect(self, arg):
        """ 決定かキャンセルかを伝えるインスタンスを設定します """
        self.outer = arg

    def initUI(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setButtons()
        self.setPathListBox()
        self.setPreviewWidget()

    def setButtons(self):
        self.btn_vbox = QVBoxLayout()
        self.btn_list = []
        #追加
        self.btn_append = QPushButton("追加")
        self.btn_append.clicked.connect(self.btn_append_clicked)
        self.btn_vbox.addWidget(self.btn_append)
        self.btn_list.append(self.btn_append)
        #追加
        self.btn_append_dir = QPushButton("追加(フォルダ内全て)")
        self.btn_append_dir.clicked.connect(self.btn_append_dir_clicked)
        self.btn_vbox.addWidget(self.btn_append_dir)
        self.btn_list.append(self.btn_append_dir)
        # #変更
        # self.btn_change = QPushButton("変更")
        # self.btn_change.clicked.connect(self.btn_change_clicked)
        # self.btn_vbox.addWidget(self.btn_change)
        # self.btn_list.append(self.btn_change)
        # #除去
        # self.btn_clear = QPushButton("除去")
        # self.btn_clear.clicked.connect(self.btn_clear_clicked)
        # self.btn_vbox.addWidget(self.btn_clear)
        # self.btn_list.append(self.btn_clear)
        #キャンセル
        self.btn_cancel = QPushButton("キャンセル")
        self.btn_cancel.clicked.connect(self.btn_cancel_clicked)
        self.btn_vbox.addWidget(self.btn_cancel)
        self.btn_list.append(self.btn_cancel)
        #OK
        self.btn_OK = QPushButton("OK")
        self.btn_OK.clicked.connect(self.btn_OK_clicked)
        self.btn_vbox.addWidget(self.btn_OK)
        self.btn_list.append(self.btn_OK)
        self.layout.addLayout(self.btn_vbox)

        for btn in self.btn_list:
            btn.setFixedWidth(160)

    def btn_append_clicked(self, event):
        fname, _ = QFileDialog.getOpenFileName(parent = self, caption = "Open File" , filter ='Image Files (*.jpg *.png *.gif)' )
        path = Path(fname)
        if path.is_file():
            print(path)
            self.imgs.add(path)
            self.path_list_widget.addItem(path.stem)

    def btn_append_dir_clicked(self, event):
        fname = QFileDialog.getExistingDirectory(parent = self, caption = "Open Directory")
        dir_path = Path(fname)
        self.imgs.addFilesByDirPath(dir_path)
        self.path_list_widget.clear()
        for img in self.imgs.getImages():
            path = img.getPath()
            self.path_list_widget.addItem(path.stem)

    def openImage(self, fileName):
        img = cv2.imread(str(fileName))
        assert not img is None
        self.cv2img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        height, width, dim = self.cv2img.shape
        self.setFixedSize(width,height)

    def btn_change_clicked(self, event):
        pass
    def btn_clear_clicked(self, event):
        pass

    def btn_cancel_clicked(self, event):
        if self.outer is None:
            self.close()
            return
        self.outer.acilsResult(ACILS_Result.Cancel)
        self.close()
    def btn_OK_clicked(self, event):
        if not self.imgs.hasAnyItems():
            d = QtWidgets.QMessageBox.warning(self," ", "ファイルを一つも読み込んでいません")
            return
        if self.outer is None:
            self.close()
            return
        self.outer.acilsResult(ACILS_Result.OK, self.imgs)
        self.close()
    def setPathListBox(self):
        self.path_list_widget = QListWidget()
        self.path_list_widget.setMinimumSize(200,400)
        self.path_list_widget.setMaximumWidth(200)

        #選択行が変わったらイベント
        self.path_list_widget.currentRowChanged.connect(self.listMove)
        #クリックされたらイベント
        self.path_list_widget.itemClicked.connect(self.listClicked)
        self.layout.addWidget(self.path_list_widget)

    def setPreview(self):
        if self.index == -1 : return
        img = self.imgs.getImage(self.index)
        self.pixmap = img.getQPixmap()
        self.preview_lbl.setPixmap(img.getQPixmap().scaledToHeight(self.height()-20))

    def listMove(self, item):
        #print(f"list moved:{item}")
        self.index = item
        self.setPreview()
    def resizeEvent(self, event):
        if self.index == -1 : return
        self.preview_lbl.setPixmap(self.pixmap.scaledToHeight(self.height()-20))

    def setPreviewWidget(self):
        self.preview_widget = QWidget()
        # self.layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout.addWidget(self.preview_widget)
        self.preview_widget.setMinimumSize(300,400)
        self.preview_layout = QHBoxLayout(self.preview_widget)
        self.preview_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.preview_lbl = QLabel("TrimerX - Version:0.0.1 -")
        self.preview_layout.addWidget(self.preview_lbl)


    def listClicked(self, item):pass
    #     print(item)
    #     print(f"list clicked:{self.path_list_widget.currentRow()}")

def main():
    app = QApplication(sys.argv)
    ex1 = AnsChkImportListSetting()
    ex1.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
