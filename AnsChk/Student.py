# -*- coding: utf-8 -*-

class Student(object):
    def __init__(self, ansmng, number, name):
        self.ansmng = ansmng
        self.number = number
        self.name = name
    def getAnsManager(self):
        return self.ansmng
    def getNumber(self):
        return self.number
    def getName(self):
        return self.name
    def getInfo(self):
        return self.number, self.name
