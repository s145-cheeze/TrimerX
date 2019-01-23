# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QDir, QPoint, QRect, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import  QApplication, QWidget, QLabel, QScrollArea, QFormLayout, QVBoxLayout, QHBoxLayout, QDialog, QPushButton, QListWidget, QStackedWidget, QMainWindow, QMenu, QMenuBar, QAction, QSpinBox

from AnsChk.Mediator import *

class AnswerCheck(QMainWindow):
    """ 切り取ったやつを表示 """
    # セットアップ-------------------------------------------------------------------
    def __init__(self, smanager = None, parent = None):
        super(AnswerCheck, self).__init__(parent)
        self.smanager = smanager
        self.anschkin = AnsChkInner()
        self.mediator = Mediator(self, smanager)

        self.initMenuBar()
        self.w = QWidget()
        self.hbox = QHBoxLayout()

        self.lst_questions = QListWidget()
        self.lst_questions.currentRowChanged.connect(self.lst_questions_moved)
        self.lst_questions.setFixedWidth(100)
        # self.lst_questions.addItem("問題")
        for ans_num in self.smanager.getAnsManageData().numbers:
            self.lst_questions.addItem(ans_num)
        self.hbox.addWidget(self.lst_questions)


        self.lst_students = QListWidget()
        self.lst_students.currentRowChanged.connect(self.lst_student_moved)
        self.lst_students.setFixedWidth(100)
        # self.lst_students.addItem("学生")
        for student in self.smanager.gets():
            self.lst_students.addItem("{} : {}".format(*student.getInfo()))
        self.hbox.addWidget(self.lst_students)


        self.hbox.addWidget(self.anschkin)


        self.w.setLayout(self.hbox)
        self.setCentralWidget(self.w)
        self.setMinimumSize(1024,768)
        self.mediator.update()

    def initMenuBar(self):
        self.m_bar = QMenuBar(self)
        menu = self.m_bar.addMenu('ファイル')
        # newAction1 = QAction("保存", self)
        # newAction1.setShortcut("Ctrl+S")
        # menu.addAction(newAction1)
        # newAction1.triggered.connect(self.newTrigger1)
        # newAction2 = QAction("別名で保存", self)
        # newAction2.setShortcut("Ctrl+Alt+S")
        # menu.addAction(newAction2)
        # newAction2.triggered.connect(self.newTrigger2)
        newAction3 = QAction("出力", self)
        newAction3.setShortcut("Ctrl+S")
        menu.addAction(newAction3)
        newAction3.triggered.connect(self.newTrigger3)
    def newTrigger1(self):
        pass
    def newTrigger2(self):
        pass
    def newTrigger3(self):
        self.smanager.export()

    def lst_student_moved(self, item):
        self.mediator.selectStudent(item)

    def lst_questions_moved(self, item):
        self.mediator.selectAnswer(item)


class AnsChkInner(QWidget):
    """docstring for AnsChkInner."""
    def __init__(self, mediator = None):
        super(AnsChkInner, self).__init__()
        self.vbox = QVBoxLayout()
        self.lbl_qno = QLabel("<h2>問</h2>")
        self.vbox.addWidget(self.lbl_qno)
        self.lbl_student = QLabel("番号 : 名前")
        self.lbl_student.setFixedWidth(self.width())
        self.lbl_student.setAlignment(Qt.AlignLeft)
        self.vbox.addWidget(self.lbl_student)
        self.hbox = QHBoxLayout()
        self.btn_prev = QPushButton("前")
        self.btn_prev.setEnabled(False)
        self.btn_prev.clicked.connect(self.prevClicked)
        self.btn_prev.setFixedWidth(20)
        self.hbox.addWidget(self.btn_prev)
        self.lbl_img = QLabel("画像はここに表示されます")
        self.lbl_img.setAlignment(Qt.AlignCenter)
        #self.lbl_img.setMinimumHeight(384)
        self.hbox.addWidget(self.lbl_img)
        self.btn_next = QPushButton("次")
        self.btn_next.setFixedWidth(20)
        self.hbox.addWidget(self.btn_next)
        self.btn_next.clicked.connect(self.nextClicked)
        self.vbox.addLayout(self.hbox)

        self.hbox2 = QHBoxLayout()
        self.jedit = QSpinBox()
        self.jedit.setValue(0)
        self.jedit.valueChanged.connect(self.jedit_valueCanged)
        self.hbox2.addWidget(self.jedit)
        self.lbl_scoring = QLabel("点/10点")
        self.hbox2.addWidget(self.lbl_scoring)
        self.vbox.addLayout(self.hbox2)

        self.setLayout(self.vbox)
    def connect(self, arg):
        self.mediator = arg

    def jedit_valueCanged(self, e):
        v = self.jedit.value()
        if v < 0:
            self.jedit.setValue(0)
            v = 0
        elif v > self.mediator.getScoring():
            self.jedit.setValue(self.mediator.getScoring())
            v = self.mediator.getScoring()
        self.mediator.setJudge(v)

    def nextClicked(self, e):
        if not self.btn_prev.isEnabled():
            self.btn_prev.setEnabled(True)
        # 画像送り
        flg = self.mediator.next()

        if flg == AnsChkInterrupt.arrived_end:
            self.btn_next.setEnabled(False)

    def prevClicked(self, e):
        if not self.btn_next.isEnabled():
            self.btn_next.setEnabled(True)

        flg = self.mediator.prev()
        if  flg == AnsChkInterrupt.arrived_top:
            self.btn_prev.setEnabled(False)


    def setAnsNum(self, txt):
        self.lbl_qno.setText(f"<h2>{txt}</h2>")
    def setStudentInfo(self, no, name):
        self.lbl_student.setText(f"{no} : {name}")
    def setAnsPixmap(self, pix):
        self.lbl_img.setPixmap(pix.scaledToWidth(720))
    def setScoring(self, txt):
        self.lbl_scoring.setText(f"点/{txt}点")
    def setJudgeEditor(self, judge):
        self.jedit.setValue(judge)






def main():
    app = QApplication(sys.argv)
    ex1 = AnswerCheck()
    ex1.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
