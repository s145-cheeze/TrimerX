# -*- coding: utf-8 -*-

from enum import Enum, auto


class AnsChkInterrupt(Enum):
    """先頭に行ったとか最後尾行ったときに伝える用"""
    no_interrupt = auto() # 何もなし
    arrived_top  = auto() # 先頭ついた
    arrived_end  = auto() # 最後尾ついた


class Mediator(object):
    """データ取ってきたり，取ってきたデータ反映したり"""
    def __init__(self, anschk, student_mng):
        self.index_student = 0
        self.index_answer  = 0
        self.anschk = anschk
        self.inner = anschk.anschkin
        self.inner.connect(self)
        self.student_mng = student_mng
        self.ansmngdata = student_mng.getAnsManageData()
    def update(self):
        # print(f"student: {self.index_student}, answer: {self.index_answer}")
        student = self.student_mng.get(self.index_student)
        ans = student.getAnsManager().get(self.index_answer)
        # 問題番号更新
        self.inner.setAnsNum(ans.getNumber())
        # 学生情報更新
        self.inner.setStudentInfo(student.getNumber(), student.getName())
        # 問題画像更新
        self.inner.setAnsPixmap(ans.getImg().getQPixmap())
        # 配点更新
        self.inner.setScoring(ans.getScoring())
        # 採点エディタ更新
        self.inner.setJudgeEditor(ans.getJudge())

        # リストボックスの位置調整
        self.anschk.lst_students.setCurrentRow(self.index_student)
        self.anschk.lst_questions.setCurrentRow(self.index_answer)

    def getScoring(self):
        student = self.student_mng.get(self.index_student)
        ans = student.getAnsManager().get(self.index_answer)
        return ans.getScoring()

    def setJudge(self, arg):
        student = self.student_mng.get(self.index_student)
        ans = student.getAnsManager().get(self.index_answer)
        ans.setJudge(arg)

    def selectStudent(self, arg):
        self.index_student = arg
        self.update()
    def selectAnswer(self, arg):
        self.index_answer = arg
        self.update()

    def next(self):
        ret = AnsChkInterrupt.no_interrupt
        self.index_student += 1
        if self.index_student >= len(self.student_mng):
            self.index_answer += 1
            self.index_student = 0
            if self.index_answer >= len(self.student_mng.getAnsManageData()) - 1:
                self.index_answer =  len(self.student_mng.getAnsManageData()) - 1
                ret = AnsChkInterrupt.arrived_end

        self.update()
        return ret
    def prev(self):
        ret = AnsChkInterrupt.no_interrupt
        self.index_student -= 1
        if self.index_student <= -1:
            self.index_answer -= 1
            self.index_student = len(self.student_mng) - 1
            if self.index_answer <= 0:
                self.index_answer = 0
                ret = AnsChkInterrupt.arrived_end

        self.update()
        return ret
