from PyQt5 import Qt, QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from FreeTrim.FreeTrimView import *


def main():
    app = QApplication(sys.argv)
    ex1 = QWidget()
    box = QVBoxLayout()
    ex1.setLayout(box)
    fmanager = FreeTrimFileManager.fromFile(ft_widget = ex1)
    for i, p in enumerate(fmanager.getImagesUsingIndex(0)):
        img, ft_id, ft_file = p
        sub_widget = FTViewSubSubWidget(ex1)
        img_name = str( "{}_{}{}".format(ft_file.getPath().stem, f"00{i}"[-2:], ft_file.getPath().suffix) )
        print(img_name)
        # ファイル名ラベル
        s = f"{i}:{img_name}"
        print(s)
        sub_widget.setImg(s, img)
        box.addWidget(sub_widget)
    ex1.show()

    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
