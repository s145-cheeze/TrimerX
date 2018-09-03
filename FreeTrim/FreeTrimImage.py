import cv2
import numpy as np

class FreeTrimImage(object):
    """docstring for FreeTrimImage."""
    def __init__(self,img,rect):
        super(FreeTrimImage, self).__init__()
        self.rect = rect
        p1 , p2 = rect.get()
        self.img = img[p1[0]:p2[0],p1[1]:p2[1],:]
    def get(self):
        return self.img
