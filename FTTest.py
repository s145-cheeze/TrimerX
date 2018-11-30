# -*- coding: utf-8 -*-

from FreeTrim.FreeTrimMain import *


def main():
    app = QApplication(sys.argv)
    ex1 = FreeTrimMain()
    ex1.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
