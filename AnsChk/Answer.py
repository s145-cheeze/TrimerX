# -*- coding: utf-8 -*-


class Answer(object):
    def __init__(self, number, scoring, judge = 0, img = None):
        # 問番号
        self.number = number
        # 配点
        self.scoring = scoring
        # 判定
        self.judge = judge
        # 回答画像
        self.img = img
    def setJudge(self, judge):
        self.judge = judge if judge <= self.scoring else self.scoring
        if self.judge < 0 : self.judge = 0
    def setImg(self, img):
        self.img = img
    def getNumber(self):
        return self.number
    def getImg(self):
        return self.img
    def getScoring(self):
        return self.scoring
    def getJudge(self):
        return self.judge
