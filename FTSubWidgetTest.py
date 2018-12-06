from FreeTrim.FreeTrimView import *


def main():
    app = QApplication(sys.argv)
    fmanager = FreeTrimFileManager.fromFile(ft_widget = None)
    ex1 = FTViewSubWidget(None, fmanager, 0)

    ex1.show()

    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
