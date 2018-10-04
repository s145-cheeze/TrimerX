# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import cv2

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton

from FreeTrimRect import *
from FreeTrimRectManager import *
from FreeTrimImage import *
from FreeTrimImageManager import *
from FreeTrimWidget import *
from FreeTrimPreview import *

class FreeTrimWindow(QWidget):
    """トリミング部分と操作ボタンの画面"""
    def __init__(self,fmanager = None, parent=None):
        super().__init__(parent)
        self.initUI()

        self.fmanager = fmanager


    def initUI(self):
        #メイン画面
        self.setGeometry(300, 300, 1024, 768)
        self.setWindowTitle('TrimerX - FreeTrimMode')
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()

        #切り取り画面
        self.ftw = FreeTrimWidget()
        self.hbox.addLayout(self.vbox)

        #
        self.loaded_image_path = Path(str(self.ftw.fname[0])).resolve()

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
    def setPreview(self):
        pass

    def listMove(self, item):
        #print(f"list moved:{item}")
        self.index = item
        self.setPreview()
    def listClicked(self, item):pass
        # print(item)
        # print(f"list clicked:{self.path_list_widget.currentRow()}")

    def saveImages(self):
        print(self.loaded_image_path.name)
        dir_name = QFileDialog.getExistingDirectory(self)
        if len(dir_name) == 0:
            return
        print(dir_name)
        for i, img in enumerate(self.ftw.imgManager.getImages()):
            img_name = str(Path(dir_name, "{}_{}{}".format(self.loaded_image_path.stem, f"00{i}"[-2:], self.loaded_image_path.suffix) ))
            print(img_name)
            cv2.imwrite(img_name, img.get()[:,:,::-1])

    def clicked_OK(self):
        print("clicked:OK")
        cv2.destroyAllWindows()
        self.preview = FreeTrimPreview(self)
        self.preview.show()


    def clicked_Undo(self):
        if not self.ftw.rectManager.hasAnyItems():
            return
        self.ftw.rectManager.pop()
        self.ftw.imgManager.pop()
        self.ftw.cls()
        self.ftw.drawAllRect()



def main():
    app = QApplication(sys.argv)
    ex1 = FreeTrimWindow()
    ex1.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
