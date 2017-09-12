# -*- coding: utf-8 -*-
# !/usr/bin/env python

import re
import requests
from bs4 import BeautifulSoup as bs
from proj1.proxygetter import GetFreeProxy
from pymongo import MongoClient

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.5',
    'Host': 'www.shfe.com.cn',
    'Connection': 'keep-alive',
}
client = MongoClient(connect=False)
db = client['data_daily']


def get_page(url, proxies=None):
    try:
        responce = requests.get(url, headers=headers, proxies=proxies)
        if responce.status_code == 200:
            return responce.json()
        return '404'
    except requests.ConnectionError as e:
        print('Get Error', e)


def parse_page(json):
    if json != '404':
        items = json.get('o_curinstrument')
        for item in items:
            res = {}
            if item['DELIVERYMONTH'] != '小计' and item['PRODUCTNAME'] != '总计':
                res['ID'] = ''.join((item['PRODUCTNAME'] + item['DELIVERYMONTH']).split())
                res['preday'] = item['PRESETTLEMENTPRICE']
                res['open'] = item['OPENPRICE']
                res['high'] = item['HIGHESTPRICE']
                res['low'] = item['LOWESTPRICE']
                res['close'] = item['CLOSEPRICE']
                res['SETTLEMENTPRICE'] = item['SETTLEMENTPRICE']
                res['ZD1_CHG'] = item['ZD1_CHG']
                res['ZD2_CHG'] = item['ZD2_CHG']
                res['volume'] = item['VOLUME']
                res['OPENINTEREST'] = item['OPENINTEREST']
                res['OPENINTERESTCHG'] = item['OPENINTERESTCHG']
                yield res


def save_to_mongo(table, results):
    collection = db[table]
    if collection.insert(results):
        print('Save to Mongo Successfully!')


def get_days(begin, end):
    import datetime
    begin_date = datetime.datetime.strptime(begin, '%Y%m%d')
    end_date = datetime.datetime.strptime(end, '%Y%m%d')
    while begin_date < end_date:
        yield begin_date.strftime('%Y%m%d')
        begin_date += datetime.timedelta(days=1)

def main(date):

    url = 'http://www.shfe.com.cn/data/dailydata/kx/kx{date}.dat'.format(date=date)
    json = get_page(url)
    res = parse_page(json)
    table = 'D' + date
    db[table].remove()
    for i in res:
        print(i)
        save_to_mongo(table, i)

if __name__ == '__main__':
    from multiprocessing.pool import Pool

    pool = Pool()
    for i in get_days('20170801', '20170901'):
        pool.apply_async(main, args=(i, ))

    pool.close()
    pool.join()