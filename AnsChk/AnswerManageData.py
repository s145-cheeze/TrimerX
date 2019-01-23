# -*- coding: utf-8 -*-

import csv

class AnswerManageData(object):
    def __init__(self, numbers, scorings):
        if len(numbers) != len(scorings):
            raise ValueError("numbers and scorings must be same length")
        self.numbers = numbers
        self.scorings = scorings
    def __len__(self):
        return len(self.numbers)
    def gets(self):
        for number, scoring in zip(self.numbers, self.scorings):
            yield number, scoring
    def get(self, index):
        return self.numbers[index], self.scorings[index]
    def getNumbers(self):
        return self.numbers
    def getScorings(self):
        return self.scorings
    @staticmethod
    def fromCSV(fname):
        numbers = []
        scorings = []
        with open(fname,"r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) != 2:
                    return None
                number, scoring = row
                numbers.append(number)
                scorings.append(int(scoring))
        return AnswerManageData(numbers,scorings)
