# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication

class menuTest(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        mbar = self.menuBar()
        mbar.setNativeMenuBar(False)
        file1 = mbar.addMenu("メニュー")
        newAction1 = QtWidgets.QAction("ぐ", self)
        newAction2 = QtWidgets.QAction("へ", self)
        newAction3 = QtWidgets.QAction("ふぁ", self)
        newAction1.setShortcut("Ctrl+N")
        newAction2.setShortcut("Ctrl+M")
        newAction3.setShortcut("Ctrl+L")
        file1.addAction(newAction1)
        file1.addAction(newAction2)
        file1.addAction(newAction3)
        newAction1.triggered.connect(self.newTrigger1)
        newAction2.triggered.connect(self.newTrigger2)
        newAction3.triggered.connect(self.newTrigger3)

        edit = self.menuBar()
        edit.setNativeMenuBar(False)
        file2 = edit.addMenu("編集")
        newAction4 = QtWidgets.QAction("取り込み", self)
        newAction5 = QtWidgets.QAction("書き込み", self)
        newAction6 = QtWidgets.QAction("切り取り", self)
        newAction4.setShortcut("Shift+N")
        newAction5.setShortcut("Shift+M")
        newAction6.setShortcut("Shift+L")
        file2.addAction(newAction4)
        file2.addAction(newAction5)
        file2.addAction(newAction6)
        newAction4.triggered.connect(self.newTrigger4)
        newAction5.triggered.connect(self.newTrigger5)
        newAction6.triggered.connect(self.newTrigger6)

    def initUI(self):
        self.setGeometry(300, 300, 720, 480)
        self.setWindowTitle('TrimerX ver1.0')
        self.show()

    def newTrigger1(self):
        print("ぐー")

    def newTrigger2(self):
        print("へー")

    def newTrigger3(self):
        print("ふぁー")

    def newTrigger4(self):
        print("取り込み中です")

    def newTrigger5(self):
        print("書き込み中です")

    def newTrigger6(self):
        print("切り取り中です")

    def closeEvent(self, event):
        #メッセージ画面の設定いろいろ
        reply = QMessageBox.question(self, 'Message',
            "本当に終了して宜しいですか？", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex1 = menuTest()
    ex1.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
