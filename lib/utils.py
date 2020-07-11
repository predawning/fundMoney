__author__ = 'leopoldli'

from datetime import date, timedelta
import os.path
from os import path


def getDateStr(days_diff=0):
    today = date.today()
    want = today + timedelta(days=days_diff)
    return want.strftime("%Y-%m-%d")

def getTodayStr():
    return getDateStr(0)

def getOneYearAgoStr():
    return  getDateStr(-365)


# print(getTodayStr(), getOneYearAgoStr())

def saveFundRanks(file_name, funds):
    head, tail = os.path.split(file_name)
    if not os.path.exists(head):
        os.makedirs(head)
    with open(file_name, 'w', encoding='utf-8') as f:
        for fund in funds:
            f.write(fund + '\n')

# 1. generate file name by, date and page, e.g. 20200710-01
# 2. check if the file exist, other wise download and write in.
def getRankFileName(date, page):
    file_name = "data/{}/{}.csv".format(date, page)
    return file_name

def isDataDownloaded(date, page):
    return path.exists(getRankFileName(date, page))

def getNextPage(date):
    MAX_PAGE = 120
    for page in range(1, MAX_PAGE):
        if not isDataDownloaded(date, page):
            return page
    return 1

ORDERWEIGHT = {'rank(3y)': 0.3,
              'rank(2y)': 0.25,
              'rank(1y)': 0.2,
              'rank(6m)': 0.15,
              'rank(1m)': 0.1}

AVERAGEWEIGHT = {'rank(3y)': 0.2,
              'rank(2y)': 0.2,
              'rank(1y)': 0.2,
              'rank(6m)': 0.2,
              'rank(1m)': 0.2}

def weightRanke(df, model='normal'):
    if model == 'normal':
        weight = ORDERWEIGHT
    else:
        weight = AVERAGEWEIGHT
    rank = 0
    for k, v in weight.items():
        rank += df[k] * v
    return rank

