# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import cv2

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget, QFileDialog, QLabel

from FreeTrimData import *
from FreeTrimFile import *
from FreeTrimFileManager import *
from FreeTrimImage import *
from FreeTrimImageManager import *
from FreeTrimImportListSetting import *
from FreeTrimPreview import *
from FreeTrimRect import *
from FreeTrimRectManager import *
from FreeTrimWidget import *
from FreeTrimWindow import *

class FreeTrimMain(QWidget):
    """ 自由トリミングのメイン画面
    起動の仕方を指定する """
    def __init__(self):
        super(FreeTrimMain, self).__init__()
        self.layout = QVBoxLayout()
        self.lbl_welcome = QLabel("<h1>TrimerX 自由トリミングモード</h1>")
        self.layout.addWidget(self.lbl_welcome)

        self.btns_layout = QVBoxLayout()
        self.layout.addLayout(self.btns_layout)

        # 読み込み画像を設定して起動
        self.btn_ftils_run = QPushButton("読み込み画像を設定して起動")
        self.btn_ftils_run.clicked.connect(self.btn_ftils_run_clicked)
        self.btns_layout.addWidget(self.btn_ftils_run)
        self.setLayout(self.layout)


        #終了
        self.btn_close = QPushButton("終了")
        self.btn_close.clicked.connect(self.close)
        self.btns_layout.addWidget(self.btn_close)
        self.setLayout(self.layout)

    def btn_ftils_run_clicked(self, event):
        # ftils = FreeTrimImportListSettingの単語の頭文字
        self.ftils = FreeTrimImportListSetting();
        self.ftils.connectFTMain(self)
        self.ftils.show()
    def ftilsResult(self, arg, files = None):
        print(f"ftilsResult {arg}")
        if arg == FTILS_Result.Cancel:
            pass
            # self.close()
        elif arg == FTILS_Result.OK:
            print([f.getFileName() for f in files.getFiles()])

            # self.ftw = FreeTrimWindow(files)
            # self.ftw.show()

def main():
    app = QApplication(sys.argv)
    ex1 = FreeTrimMain()
    ex1.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
