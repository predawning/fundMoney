__author__ = 'leopoldli'

import re
import time

import requests

from lib import utils

url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft={}&rs=&gs=0&sc={}&st=desc&sd={}&ed={}&qdii=&tabSubtype=,,,,,&pi={}&pn=50&dx=1'
header = {}

s = '''Accept: */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: keep-alive
Cookie: searchbar_code=161726; qgqp_b_id=5644c99a877815eaa2d21ac1dddd8637; cowminicookie=true; intellpositionL=80%25; intellpositionT=656px; st_si=90640908928289; st_asi=delete; ASP.NET_SessionId=v5g2ppwo1yi40k2lawlfdzif; st_pvi=63444169218271; st_sp=2020-01-20%2023%3A37%3A16; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=3; st_psi=20200522204019144-112200304021-9968676370
Host: fund.eastmoney.com
Referer: http://fund.eastmoney.com/data/fundranking.html
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'''

for line in s.split('\n'):
    header[line.split(': ')[0]] = line.split(': ')[1]

today = utils.getTodayStr()
oneYearAgo = utils.getOneYearAgoStr()
scArg = '3nzf' # 1nzf 2nzf
ftArg = 'all'  # gp, hh, zq, zs

MAX_PAGE = 120
SLEEP = 1

for page in range(utils.getNextPage(today), MAX_PAGE + 1):
    link = url.format(ftArg, scArg, oneYearAgo, today, page)
    res = requests.get(link, headers=header)
    datas = ['基金代码,基金名字,名字缩写,日期,单位净值,累计净值,日增长率,近一周,近1月,近3月,近6月,近1年,近2年,近3年,今年来,成立来,成立日,买入后锁定期,自定义,原费率,手续费,折扣,手续费,折扣,不知道']
    datas += eval(re.findall('\[.*?\]', res.text, re.S)[0])
    fn = utils.getRankFileName(today, page)
    utils.saveFundRanks(fn, datas)
    print('downloaded %s' % fn)
    time.sleep(SLEEP)
