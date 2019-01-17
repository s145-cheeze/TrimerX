# -*- coding: utf-8 -*-

from copy import deepcopy

from AnsChk.AnswerManageData import *
from AnsChk.AnswerManager import *

class AnswerManagerFactory(object):
    def __init__(self, ansmngdata):
        self.ansmngdata = ansmngdata
    def create(self):
        cp_ansmngdata = deepcopy(self.ansmngdata)
        return AnswerManagerBuilder(cp_ansmngdata)
