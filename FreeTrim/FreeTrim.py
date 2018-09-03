from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton

from FreeTrimRect import *
from FreeTrimRectData import *
from FreeTrimImage import *
from FreeTrimImageData import *
from FreeTrimWindow import *

class FreeTrim(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()


    def initUI(self):
        self.setGeometry(300, 300, 720, 480)
        self.setWindowTitle('TrimerX - FreeTrimMode')
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()

        self.ftw = FreeTrimWindow()
        self.hbox.addLayout(self.vbox)

        self.btnOK = QPushButton('OK')
        self.btnOK.clicked.connect(self.clicked_OK)
        self.vbox.addWidget(self.btnOK)

        self.btnUndo = QPushButton('一つ戻す')
        self.btnUndo.clicked.connect(self.clicked_Undo)
        self.vbox.addWidget(self.btnUndo)

        self.hbox.addWidget(self.ftw)

        self.setLayout(self.hbox)
        self.show()
    def clicked_OK(self):
        print("clicked: OK")
    def clicked_Undo(self):
        if not self.ftw.rectData.hasAnyItems():
            return 
        self.ftw.rectData.pop()
        self.ftw.imgData.pop()
        self.ftw.cls()
        self.ftw.drawAllRect()


def main():
    app = QApplication(sys.argv)
    ex1 = FreeTrim()
    ex1.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
