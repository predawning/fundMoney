__author__ = 'leopoldli'


import glob

import pandas as pd

all_files = glob.glob("data/f10/*.csv")
all_files.sort()

li = []
for filename in all_files[:80]:
    df = pd.read_csv(filename, index_col=None, dtype={'code': str})
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
stock = '立讯精密'
df = frame[frame[stock].notna()].sort_values(by=stock, ascending=False)
print(df[["基金简称", stock]])


