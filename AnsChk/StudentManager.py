# -*- coding: utf-8 -*-

import pickle
import sys
import csv
import datetime
from pathlib import Path

import cv2

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from AnsChk.Student import *
from AnsChk.AnswerManagerFactory import *

class StudentManager(object):
    def __init__(self, ansmngdata):
        self.students = []
        self.ansmngfactory = AnswerManagerFactory(ansmngdata)
    def __len__(self):
        return len(self.students)
    def create(self, number, name):
        ansmng = self.ansmngfactory.create()
        student  = Student(ansmng, number, name)
        self.students.append(student)
    def setImages(self, imgs):
        cnt=0
        for student in self.students:
            ansmng = student.getAnsManager()
            for ans in ansmng.gets():
                try:
                    ans.setImg(imgs.getImage(cnt))
                except IndexError as e:
                    return False
                cnt += 1
        return True
    def gets(self):
        for student in self.students:
            yield student
    def get(self, index):
        return self.students[index]
    def getAnsManageData(self):
        return self.ansmngfactory.getAnsManageData()
    def export(self):
        fname, _ = QFileDialog.getSaveFileName(parent = None, caption = "Save File" , filter ='CSV File (*.csv)',
                directory = './TrimerXAnswerCheckExportData({}).csv'.format(
                        datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                    )
                )
        if fname is None:
            return -1
        with open(fname,"w",encoding="utf-8") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(["No.","Name"] + self.ansmngfactory.getAnsManageData().getNumbers())
            for student in self.students:
                info = [str(student.getNumber()), str(student.getName())]
                writer.writerow(info + student.getAnsManager().getJudges())


    # def saveFile(self, arg):
    #     fname, _ = QFileDialog.getSaveFileName(parent = None, caption = "Save File" , filter ='TrimerX Answer Check Data (*.txacd)',
    #         directory = './TrimerXAnswerCheckData({}).txacd'.format(
    #                 datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    #             )
    #         )
    #     with open(fname,"wb") as f:
    #         pickle.dump(self, f)
    @staticmethod
    def fromCSV(ansmngdata, fname):
        smng = StudentManager(ansmngdata)
        with open(fname,"r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) != 2:
                    return None
                smng.create(*row)
        return smng
    # @staticmethod
    # def loadFile(self):
    #     fname , _ =QFileDialog.getOpenFileName(parent = None, caption = "Open File" , filter ='TrimerX Answer Check Data (*.txacd)')
    #     with open(fname,"rb") as var:
    #         passa
