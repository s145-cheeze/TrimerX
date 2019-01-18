from FreeTrim.FreeTrimView import *


def main():
    app = QApplication(sys.argv)
    ex1 = FreeTrimView()
    ex1.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
