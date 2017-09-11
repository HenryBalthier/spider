# -*- coding: utf-8 -*-
# !/usr/bin/env python

import re
import requests
from bs4 import BeautifulSoup as bs
from pyquery import PyQuery as pq
from pymongo import MongoClient
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.5',
    'Host': 'futures.eastmoney.com',
    'Connection': 'keep-alive',
}

client = MongoClient()
db = client['news_daily']

def get_page(url):
    try:
        responce = requests.get(url, headers=headers)
        if responce.status_code == 200:
            return responce.text
        else:
            return '404'
    except requests.ConnectionError:
        pass


def urlchecker(url):
    if url is None:
        return False
    pattern = r".*?/news/\d+,\d+.html"
    return True if re.match(pattern, url) else False


def titles(url):
    html = get_page(url)
    p = pq(html)

    url_list = []
    for i in p("li"):
        d = {}
        q = pq(i).find('p').find('a')
        if urlchecker(pq(q).attr('href')):
            url_list.append([pq(q).attr('href'), pq(q).text()])
            d['ID'] = pq(q).attr('href').split(',')[1].split('.')[0]
            d['title'] = pq(q).text()
            d['url'] = pq(q).attr('href')
            d['details'] = ''
            #print(d)
            yield d


def articles(dct):
    table = 'T' + dct['ID'][0:8]
    html = get_page(dct['url'])
    p = pq(html)

    for i in p('p'):
        dct['details'] += pq(i).text()
        #print(pq(i).text())

    print(dct)
    save_to_mongo(table, dct)


def save_to_mongo(table, results):
    collection = db[table]
    if collection.insert(results):
        print('Save to Mongo Successfully!')


if __name__ == '__main__':
    page = 1
    for i in range(page):
        pagenumber = '_' + str(i) if i > 0 else ''
        url = 'http://futures.eastmoney.com/news/cqhdd{}.html'.format(pagenumber)
        for j in titles(url):
            articles(j)
