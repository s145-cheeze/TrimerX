from PyQt5 import QtWidgets

from FreeTrimRect import *
from FreeTrimRectData import *
from FreeTrimWindow import *

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex1 = FreeTrimWindow()
    ex1.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
