__author__ = 'leopoldli'

import pandas as pd
import os.path
import time

from datetime import datetime, timedelta

def getF10FileName(code, dir='f10'):
    return 'data/{}/{}.csv'.format(dir, code)

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)

def getSharpRate(code):
    url2 = 'http://fund.eastmoney.com/f10/tsdata_{}.html'.format(code)
    tables2 = pd.read_html(url2, encoding='utf-8')
    df = tables2[1]
    df_fin3 = df.loc[[2], [1, 2, 3]]
    df_fin3.columns = ['夏普比率(近1年)', '夏普比率(近2年)', '夏普比率(近3年)']
    df_fin3['code'] = code
    df_fin3.set_index('code', inplace=True)
    return df_fin3

def getF10Detail(code):
    url = 'http://fund.eastmoney.com/f10/{}.html'.format(code)
    tables = pd.read_html(url, encoding='utf-8')
    df = tables[1]
    df1 = df[[0, 1]]
    df2 = df[[2, 3]]
    df1.set_index(0, inplace=True)
    df2.set_index(2, inplace=True)
    df1 = df1.T
    df2 = df2.T
    df1['code'] = code
    df2['code'] = code
    df1.set_index('code', inplace=True)
    df2.set_index('code', inplace=True)
    df_fin2 = pd.concat([df1, df2], axis=1)
    return df_fin2

def getPosition(code):
    url3 = 'http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=jjcc&code={}&topline=10&year=2020'.format(code)
    tables3 = pd.read_html(url3, encoding='utf-8', converters={'股票代码': str})
    df = tables3[0]
    df2 = df[["占净值比例"]]
    df2 = df2.T
    df2.columns = df["股票名称"]
    df2['code'] = code
    df2.set_index('code', inplace=True)
    return df2

def getF10FromRemote(code):
    time.sleep(0.5)
    print("fetch f10 for fund %s" % code)
    df_fin3 = getSharpRate(code)
    df_fin2 = getF10Detail(code)

    df_fin4 = df_fin2.combine_first(df_fin3)
    df_fin4['基金代码'] = code

    df = getPosition(code)
    positions = "|".join(df.columns)
    df_fin4['持仓'] = positions
    df_fin4 = df_fin4.combine_first(df)
    return df_fin4

# print(getF10FromRemote('213001'))

def getF10FromLocal(code):
    df = pd.read_csv(getF10FileName(code), dtype={'code': str})
    return df

def isF10LocalCached(code):
    file = getF10FileName(code)
    bench = datetime.now() - timedelta(days=10)
    return os.path.exists(file) and bench<modification_date(file)

def getF10Data(code, fresh=False):
    if not isF10LocalCached(code) or fresh:
        df = getF10FromRemote(code)
        file = getF10FileName(code)
        df.to_csv(file, encoding='utf-8')
    return getF10FromLocal(code)

# df = getF10Data('161903')
# print(df)


f10_cols = ['code', '业绩比较基准', '份额规模', '发行日期', '基金代码', '基金全称', '基金托管人', '基金简称', '基金管理人',
            '基金类型', '基金经理人', '夏普比率(近1年)', '夏普比率(近2年)', '夏普比率(近3年)', '成立日期/规模',
            '成立来分红', '托管费率', '最高申购费率', '最高认购费率', '最高赎回费率', '管理费率', '资产规模', '跟踪标的',
            '销售服务费率', '持仓']

def getF10DataDF(codes, fresh=False):
    li = []
    for code in codes:
        df = getF10Data(code, fresh)
        df = df[f10_cols]
        li.append(df)
    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.set_index('code', inplace=True)
    return frame

