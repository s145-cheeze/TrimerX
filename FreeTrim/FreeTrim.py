# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import cv2

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton

from FreeTrimRect import *
from FreeTrimRectData import *
from FreeTrimImage import *
from FreeTrimImageData import *
from FreeTrimWindow import *
from FreeTrimPreview import *

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

        self.loaded_image_path = Path(str(self.ftw.fname[0])).resolve()

        self.btnOK = QPushButton('OK')
        self.btnOK.clicked.connect(self.clicked_OK)
        self.vbox.addWidget(self.btnOK)

        self.btnUndo = QPushButton('一つ戻す')
        self.btnUndo.clicked.connect(self.clicked_Undo)
        self.vbox.addWidget(self.btnUndo)

        self.hbox.addWidget(self.ftw)

        self.setLayout(self.hbox)
        self.show()

    def saveImages(self):
        print(self.loaded_image_path.name)
        dir_name = QFileDialog.getExistingDirectory(self)
        if len(dir_name) == 0:
            return
        print(dir_name)
        for i, img in enumerate(self.ftw.imgData.getImages()):
            img_name = str(Path(dir_name, "{}_{}{}".format(self.loaded_image_path.stem, f"00{i}"[-2:], self.loaded_image_path.suffix) ))
            print(img_name)
            cv2.imwrite(img_name, img.get()[:,:,::-1])

    def clicked_OK(self):
        print("clicked:OK")
        cv2.destroyAllWindows()
        self.preview = FreeTrimPreview(self)
        self.preview.show()


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
