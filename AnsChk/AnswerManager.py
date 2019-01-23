# -*- coding: utf-8 -*-

from AnsChk.Answer import *

class AnswerManager(object):
    def __init__(self, ansmngdata):
        self.ansmngdata = ansmngdata
        self.answers = [Answer(*data) for data in self.ansmngdata.gets()]
    def gets(self):
        for ans in self.answers:
            yield ans
    def getJudges(self):
        return [ans.getJudge() for ans in self.answers]
    def get(self, index):
        return self.answers[index]
