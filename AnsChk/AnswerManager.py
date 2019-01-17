# -*- coding: utf-8 -*-

from Anschk.Answer import *

class AnswerManager(object):
    def __init__(self, ansmngdata):
        self.ansmngdata = ansmngdata
        self.judges = [0 for i in range(len(ansmngdata))]
        self.answers = [Answer(*data) for data in self.ansmngdata.gets()]
    def gets(self):
        for cnt, t in enumerate(self.ansmngdata.gets()):
            number, scoring = t
            judge = self.judges[cnt]
            yield number, scoring, judge
    def get(self, index):
        number, scoring = self.ansmngdata.get(index)
        return number, scoring, self.judges[index]
    def getAnswer(self, index):
        return self.answers[index]
