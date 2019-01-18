# -*- coding: utf-8 -*-

from AnsChk.Student import *
from AnsChk.AnswerManagerFactory import *

class StudentManager(object):
    def __init__(self, ansmngdata):
        self.students = []
        self.ansmngfactory = AnswerManagerFactory(ansmngdata)
    def create(self, number, name):
        ansmng = self.ansmngfactory.create()
        student  = Student(ansmng, number, name)
        self.students
    def gets(self):
        for student in self.students:
            yield student
    def get(self, index):
        return self.students[index]
    @staticmethod
    def fromCSV(ansmngdata, fname):
        smng = StudentManager(ansmngdata)
        with open(fname,"r") as f:
            reader = csv.reader(f)
            for row in reader:
                smng.create(*row)
