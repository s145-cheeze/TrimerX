# -*- coding: utf-8 -*-

from AnsChk.Main import *


def main():
    app = QApplication(sys.argv)
    ex1 = AnswerCheckMain()
    ex1.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
