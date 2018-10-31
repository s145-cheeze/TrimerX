# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import cv2

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton, QListWidget, QAction, QMenuBar

from FreeTrim.FreeTrimRect import *
from FreeTrim.FreeTrimRectManager import *
from FreeTrim.FreeTrimImage import *
from FreeTrim.FreeTrimImageManager import *
from FreeTrim.FreeTrimFileManager import *
from FreeTrim.FreeTrimWidget import *
from FreeTrim.FreeTrimPreview import *

class FreeTrimWindow(QWidget):
    """トリミング部分と操作ボタンの画面"""
    def __init__(self,fmanager = None, parent=None):
        super().__init__(parent)
        self.fmanager = fmanager
        self.initUI()
        self.initMenuBar()
        self.updatePathListBox()

    def initMenuBar(self):
        self.m_bar = QMenuBar(self)
        menu = self.m_bar.addMenu('ファイル')
        newAction1 = QAction("保存", self)
        newAction1.setShortcut("Ctrl+S")
        menu.addAction(newAction1)
        newAction1.triggered.connect(self.newTrigger1)
        newAction2 = QAction("別名で保存", self)
        newAction2.setShortcut("Ctrl+Alt+S")
        menu.addAction(newAction2)
        newAction2.triggered.connect(self.newTrigger1)

    def newTrigger1(self):
        self.fmanager.saveFile(False)
    def newTrigger2(self):
        self.fmanager.saveFile(True)



    def initUI(self):
        #メイン画面
        self.setGeometry(300, 300, 1024, 768)
        self.setWindowTitle('TrimerX - FreeTrimMode')
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()

        #切り取り画面
        self.ftw = FreeTrimWidget(self.fmanager)
        self.hbox.addLayout(self.vbox)



        self.btnOK = QPushButton('OK')
        self.btnOK.clicked.connect(self.clicked_OK)
        self.vbox.addWidget(self.btnOK)

        self.btnUndo = QPushButton('一つ戻す')
        self.btnUndo.clicked.connect(self.clicked_Undo)
        self.vbox.addWidget(self.btnUndo)

        #メイン画面
        self.scrollArea = QScrollArea()
        self.inner = QWidget()
        self.inner_layout = QVBoxLayout()
        self.inner.setLayout(self.inner_layout)

        self.inner_layout.addWidget(self.ftw)

        self.scrollArea.setWidget(self.inner)

        self.hbox.addWidget(self.scrollArea)

        self.setPathListBox()
        self.setLayout(self.hbox)
        self.show()
    def setPathListBox(self):
        self.path_list_widget = QListWidget()
        self.path_list_widget.setMinimumSize(200,400)
        self.path_list_widget.setMaximumWidth(200)

        #選択行が変わったらイベント
        self.path_list_widget.currentRowChanged.connect(self.listMove)
        #クリックされたらイベント
        self.path_list_widget.itemClicked.connect(self.listClicked)
        self.vbox.addWidget(self.path_list_widget)
    def updatePathListBox(self):
        self.path_list_widget.clear()
        for path in self.fmanager.getFiles():
            self.path_list_widget.addItem(path.getFileName())
    def setPreview(self):
        pass

    def listMove(self, item):
        #print(f"list moved:{item}")
        self.index = item
        self.fmanager.setCurrent(self.index)
        self.ftw.changeImage()
        self.setPreview()
    def listClicked(self, item):
        pass

        # print(item)
        # print(f"list clicked:{self.path_list_widget.currentRow()}")


    def clicked_OK(self):
        print("clicked:OK")
        #cv2.destroyAllWindows()
        self.preview = FreeTrimPreview(self.fmanager, self)
        self.preview.show()


    def clicked_Undo(self):
        if not self.ftw.rect_manager.hasAnyItems():
            return
        self.ftw.rect_manager.pop()
        self.ftw.img_manager.pop()
        self.ftw.cls()
        self.ftw.drawAllRect()



def main():
    app = QApplication(sys.argv)
    fmanager = FreeTrimFileManager()
    fmanager.addFileDilalog()
    ex1 = FreeTrimWindow(fmanager)
    ex1.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
