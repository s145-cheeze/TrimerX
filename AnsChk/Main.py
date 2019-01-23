# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import  QApplication, QWidget, QLabel, QScrollArea, QFormLayout, QVBoxLayout, QHBoxLayout, QDialog, QPushButton, QListWidget, QStackedWidget

from AnsChk.AnsChkImportListSetting import *
from AnsChk.FileForm import *
from AnsChk.StudentManager import *
from AnsChk.AnswerCheck import *



class AnswerCheckMain(QWidget):
    def __init__(self):
        super(AnswerCheckMain, self).__init__()

        self.fmanager = None

        self.initUI()
    def initUI(self):
        self.layout = QVBoxLayout()
        self.lbl_title = QLabel("<h1>TrimerX 採点モード</h1>")
        self.layout.addWidget(self.lbl_title)

        self.btns_layout = QVBoxLayout()

        self.btn_acils_run = QPushButton("起動")
        self.btn_acils_run.clicked.connect(self.btn_acils_run_clicked)
        self.btns_layout.addWidget(self.btn_acils_run)

        # self.btn_import_FTData = QPushButton("途中データを読み込みして起動")
        # self.btn_import_FTData.clicked.connect(self.btn_import_FTData_clicked)
        # self.btns_layout.addWidget(self.btn_import_FTData)

        #終了
        self.btn_close = QPushButton("終了")
        self.btn_close.clicked.connect(self.close)
        self.btns_layout.addWidget(self.btn_close)

        self.layout.addLayout(self.btns_layout)
        self.setLayout(self.layout)

    def btn_acils_run_clicked(self, event):
        self.ff = FileForm();
        self.ff.show()








def main():
    app = QApplication(sys.argv)
    ex1 = FreeTrimPreview(FreeTrimImageManager())
    ex1.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
