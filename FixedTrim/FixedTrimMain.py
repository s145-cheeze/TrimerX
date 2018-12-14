# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import cv2

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget, QFileDialog, QLabel

#from FixedTrim.FixedTrimWidget import *
from FixedTrim.FixedTrimWindow import *

class FixedTrimMain(QWidget):
    """ 自由トリミングのメイン画面
    起動の仕方を指定する """
    def __init__(self):
        super(FixedTrimMain, self).__init__()

        self.fmanager = None

        self.initUI()
    def initUI(self):
        self.layout = QVBoxLayout()
        self.lbl_title = QLabel("<h1>TrimerX 自由トリミングモード</h1>")
        self.layout.addWidget(self.lbl_title)

        self.btns_layout = QVBoxLayout()
        self.layout.addLayout(self.btns_layout)

        # 読み込み画像を設定して起動
        self.btn_ftils_run = QPushButton("読み込み画像を設定して起動")
        self.btn_ftils_run.clicked.connect(self.btn_ftils_run_clicked)
        self.btns_layout.addWidget(self.btn_ftils_run)
        self.setLayout(self.layout)
        # 切り取りデータを読み込みして起動
        self.btn_import_FTData = QPushButton("切り取りデータを読み込みして起動")
        self.btn_import_FTData.clicked.connect(self.btn_import_FTData_clicked)
        self.btns_layout.addWidget(self.btn_import_FTData)
        self.setLayout(self.layout)


        #終了
        self.btn_close = QPushButton("終了")
        self.btn_close.clicked.connect(self.close)
        self.btns_layout.addWidget(self.btn_close)
        self.setLayout(self.layout)

    def btn_ftils_run_clicked(self, event):
        self.fmanager = FixedTrimFileManager()
        # ftils = FixedTrimImportListSettingの単語の頭文字
        self.ftils = FixedTrimImportListSetting(self.fmanager);
        self.ftils.connectFTMain(self)
        self.ftils.show()
    def btn_import_FTData_clicked(self, event):
        fmanager = FixedTrimFileManager.fromFile(ft_widget = self)
        if fmanager == -1:
            pass
        else:
            self.fmanager = fmanager
            self.ftw = FixedTrimWindow(self.fmanager)
            self.ftw.show()
    def ftilsResult(self, arg, fmanager = None):
        print(f"ftilsResult {arg}")
        if arg == FTILS_Result.Cancel:
            self.fmanager = None
            # self.close()
        elif arg == FTILS_Result.OK:
            print([f.getFileName() for f in self.fmanager.getFiles()])
            self.ftw = FixedTrimWindow(self.fmanager)
            self.ftw.show()

            # self.ftw = FixedTrimWindow(fmanager)
            # self.ftw.show()

def main():
    app = QApplication(sys.argv)
    ex1 = FixedTrimMain()
    ex1.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
