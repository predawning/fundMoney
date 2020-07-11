__author__ = 'leopoldli'

import pandas as pd
import urllib.request
import re


from selenium import webdriver
browser = webdriver.Chrome()
url = 'https:www.baidu.com'
browser.get(url)#打开浏览器预设网址
print(browser.page_source)#打印网页源代码
browser.close()#关闭浏览器


