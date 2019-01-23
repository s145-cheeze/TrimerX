# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import  QApplication, QWidget, QLabel, QScrollArea, QFormLayout, QVBoxLayout, QHBoxLayout, QDialog, QPushButton, QListWidget, QStackedWidget, QMainWindow, QMenu, QMenuBar, QAction, QFormLayout, QLineEdit, QFileDialog, QDialogButtonBox

from AnsChk.AnswerManageData import *
from AnsChk.StudentManager import *
from AnsChk.Images import *
from AnsChk.AnswerCheck import *
from AnsChk.AnsChkImportListSetting import *

class FileForm(QWidget):
    def __init__(self, parent = None):
        super(FileForm, self).__init__(parent)

        self.imgs = None

        self.form = QFormLayout()
        self.fs_answer = FileSelect()
        self.form.addRow("問題データ(csv)", self.fs_answer)
        self.fs_student = FileSelect()
        self.form.addRow("学生データ(csv)", self.fs_student)
        self.fs_actils = ImageSelect(self)
        self.form.addRow("画像データ(別ウィンドウが開きます)", self.fs_actils)
        self.btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.btn_box.accepted.connect(self.OK)
        self.btn_box.rejected.connect(self.canel)
        self.form.addWidget(self.btn_box)
        self.setLayout(self.form)

    def connect(self, arg):
        self.outer = arg

    def OK(self):
        if self.fs_student.getFileName() == "" or self.fs_answer.getFileName() == "" or self.imgs is None:
            d = QtWidgets.QMessageBox.warning(self," ", "読み込むデータを指定してください")
            return
        ansdatapath = self.fs_answer.getFileName()
        ansmngdata = AnswerManageData.fromCSV(ansdatapath)
        if ansmngdata is None:
            d = QtWidgets.QMessageBox.warning(self," ", "問題データの読み込み関連でエラーが発生しました")
            return
        studentdatapath = self.fs_student.getFileName()
        smng = StudentManager.fromCSV(ansmngdata, studentdatapath)
        if smng is None:
            d = QtWidgets.QMessageBox.warning(self," ", "学生データの読み込み関連でエラーが発生しました")
            return
        t = smng.setImages(self.imgs)
        if not t:
            d = QtWidgets.QMessageBox.warning(self," ", "画像の数が足りません")
            return
        AnswerCheck(smng).show()
        self.close()


    def setImages(self, arg):
        self.imgs = arg


    def canel(self):
        self.close()

class FileSelect(QWidget):
    def __init__(self, parent = None):
        super(FileSelect, self).__init__(parent)
        self.ffilter = "CSV File (*.csv)"
        self.fname = "FileName.csv"

        self.hbox = QHBoxLayout()
        self.fedit = QLineEdit()
        self.fedit.setText(self.fname)
        self.hbox.addWidget(self.fedit)
        self.btn = QPushButton("...")
        self.btn.clicked.connect(self.btn_clicked)
        self.hbox.addWidget(self.btn)
        self.setLayout(self.hbox)
    def getFileName(self):
        if self.fname != self.fedit.text():
            self.fname = self.fedit.text()
        return self.fname
    def btn_clicked(self, e):
        fname , _ = QFileDialog.getOpenFileName(parent = None, caption = "Open File" , filter = self.ffilter)
        self.fname = fname
        self.fedit.setText(fname)

class ImageSelect(FileSelect):
    def __init__(self, fileform, parent = None):
        super(ImageSelect, self).__init__(parent)
        self.fileform = fileform
        self.fedit.setText("未選択")
    def btn_clicked(self, e):
        self.imgs = Images()
        # acils = AnsChkImportListSettingの単語の頭文字
        self.acils = AnsChkImportListSetting(self.imgs);
        self.acils.connect(self)
        self.acils.show()
    def acilsResult(self, arg, imgs = None):
        if arg == ACILS_Result.Cancel:
            self.imgs = None
        elif arg == ACILS_Result.OK:
            self.fileform.setImages(imgs)
            self.fedit.setText("選択済み")



def main():
    app = QApplication(sys.argv)
    ex1 = FileFrom()
    ex1.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
