from FreeTrim.FreeTrimView import *


def main():
    app = QApplication(sys.argv)
    ex1 = FTViewSubSubWidget()
    fmanager = FreeTrimFileManager.fromFile(ft_widget = ex1)
    for i, p in enumerate(fmanager.getImagesUsingIndex(0)):
        img, ft_id, ft_file = p
        img_name = str( "{}_{}{}".format(ft_file.getPath().stem, f"00{i}"[-2:], ft_file.getPath().suffix) )
        print(img_name)
        # ファイル名ラベル
        s = f"{i}:{img_name}"
        print(s)
        ex1.setImg(s, img)
        break
    ex1.show()

    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
