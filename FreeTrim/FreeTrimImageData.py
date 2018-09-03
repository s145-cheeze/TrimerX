from FreeTrimImage import *


class FreeTrimImageData(object):
    """docstring for FreeTrimImageData."""
    def __init__(self):
        super(FreeTrimImageData, self).__init__()
        self.imgs = []
    def getImages(self):
        for img in self.imgs:
            yield img
    def newImage(self, img, rect):
        img = FreeTrimImage(img, rect)
        self.imgs.append(img)
        return img
