import time
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import HTTPError
from urllib import parse
import chardet
import math
import numpy as np
from django.shortcuts import render


def craw():
    news = bs.find_all('dl', {'class': 'newsList'})

    news_list = []
    news_list_2 = []
    title_list = []
    title_list_2 = []
    url_list = []
    url_list_2 = []

    for new in news:
        title = new.find_all('dt', {'class': 'articleSubject'})
        title_2 = new.find_all('dd', {'class': 'articleSubject'})
        date_time = new.find_all('dd', {'class': 'articleSummary'})

        for dt in title:
            dd = dt.text[1:-1]
            link = dt.find("a")["href"]
            article_url = 'https://finance.naver.com/' + link

            #             text_list = [dd, article_url]
            url_list.append(article_url)
            title_list.append(dd)
        #             news_list.append(text_list)

        for oo in title_2:
            #         title.append(new.text[1:-1])
            article_title = oo.text[1:-1]
            link = oo.find("a")["href"]
            article_url = 'https://finance.naver.com/' + link

            text_list = [article_title, article_url]
            url_list_2.append(article_url)
            title_list_2.append(article_title)
        #             news_list_2.append(text_list)

        url_result = [url_list, url_list_2]
        title_result = [title_list, title_list_2]
    return url_result, title_result


search = "케티"
stDateStart = "2018-01-01"
stDateEnd = "2022-07-20"

# 검색어 인코딩
euc_data = search.encode('euc-kr')
tmp = str(euc_data).replace("\\x", "%")[2:-1]

# 여러 페이지 크롤링

hh = []

url = f"https://finance.naver.com/news/news_search.nhn?rcdate=&q={tmp}\
    &x=5&y=7&sm=all.basic&pd=1&&&page="

req = requests.get(url)
bs = BeautifulSoup(req.content, "html.parser")

strong = bs.find_all('strong')
article_num = strong[-3]
article_num = int(article_num.text)
i = math.ceil(article_num / 20)

tmp3 = []
print(article_num)
i += 1

for page in range(1, i):
    url = f"https://finance.naver.com/news/news_search.nhn?rcdate=&q={tmp}\
        &x=5&y=7&sm=all.basic&pd=1&{stDateStart}&{stDateEnd}&page={page}"

    req = requests.get(url)
    bs = BeautifulSoup(req.content, "html.parser")

    # 기사 갯수 파악 후 for문 범위 정하기

    url_list, title_list = craw()

    url_list = [y for x in url_list for y in x]
    title_list = [y for x in title_list for y in x]

    for j in range(len(url_list)):
        tmp2 = []
        tmp2.append(url_list[j])
        tmp2.append(title_list[j])
        tmp3.append(tmp2)
        #print(url)
tmp3 = pd.DataFrame(tmp3)
tmp3.to_csv("이지케어텍_url.csv")


def crawl(request):
    return render(request,"crawl.html")
