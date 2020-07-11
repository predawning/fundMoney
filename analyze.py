__author__ = 'leopoldli'
import glob

import pandas as pd

from lib import fund_detail, utils

today = utils.getTodayStr()
all_files = glob.glob("data/{}/*.csv".format(today))
all_files.sort()

fmt = 'xls'
fmt = 'csv'
model = 'average'
model = 'normal'
report = 'data/{}-top20funds-{}.{}'.format(today, model, fmt)
debug_report = 'data/{}-debug-{}.{}'.format(today, model, fmt)
fresh = False

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, dtype={'基金代码': str})
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
frame['code'] = frame['基金代码']

rate_year = 1/6
rate_month = 1/5
total_rows = len(frame)
year_number = int(rate_year*total_rows)
month_number = int(rate_month*total_rows)
three_year_funds = frame.nlargest(year_number, '近3年').reset_index(drop=True)
three_year_funds['rank(3y)'] = three_year_funds.index + 1

two_year_funds = frame.nlargest(year_number, '近2年').reset_index(drop=True)
two_year_funds['rank(2y)'] = two_year_funds.index + 1

one_year_funds = frame.nlargest(year_number, '近1年').reset_index(drop=True)
one_year_funds['rank(1y)'] = one_year_funds.index + 1
six_month_funds = frame.nlargest(month_number, '近6月').reset_index(drop=True)
six_month_funds['rank(6m)'] = six_month_funds.index + 1
three_month_funds = frame.nlargest(month_number, '近3月').reset_index(drop=True)
three_month_funds['rank(3m)'] = three_month_funds.index + 1
one_month_funds = frame.nlargest(month_number, '近1月').reset_index(drop=True)
one_month_funds['rank(1m)'] = one_month_funds.index + 1

df1 = pd.merge(three_year_funds, two_year_funds)
df2 = pd.merge(df1, one_year_funds)
df3 = pd.merge(df2, six_month_funds)
df4 = pd.merge(df3, three_month_funds)
df5 = pd.merge(df4, one_month_funds)
print('shrink speed: ', total_rows, len(df1), len(df2), len(df3), len(df4), len(df5))
codes = df5["基金代码"]

# print('fetch codes', codes)
df5.set_index('code', inplace=True)

df_fin4 = fund_detail.getF10DataDF(codes, fresh)
df_fin4 = df5.combine_first(df_fin4)
df_fin4['rank'] = utils.weightRanke(df_fin4, model)

df_fin4.sort_values(by='rank', inplace=True)
df_debug = df_fin4
df_debug = df_fin4.loc[df_fin4['基金管理人']=='广发基金']
df_debug.to_csv(debug_report, encoding='utf-8', index=True)
df_fin5 = df_fin4[:50]

cols = ['基金简称', '基金管理人', '基金类型', '基金经理人',
        'rank(3y)', 'rank(2y)', 'rank(1y)', 'rank(6m)', 'rank(3m)', 'rank',
        '近3年', '近2年', '近1年', '近6月', '近3月',
        '夏普比率(近3年)', '夏普比率(近2年)', '夏普比率(近1年)', '资产规模']
df_fin6 = df_fin5.sort_values(by=['夏普比率(近3年)', '夏普比率(近2年)', '夏普比率(近1年)'], ascending=False)
df_fin7 = df_fin6[:20][cols]
if fmt == 'csv':
    df_fin7.to_csv(report, encoding='utf-8', index=True)
else:
    df_fin7.to_excel(report, encoding='utf-8', index=True)


