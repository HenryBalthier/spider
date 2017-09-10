# -*- coding: utf-8 -*-
# !/usr/bin/env python

import re
import requests
from bs4 import BeautifulSoup as bs
#from multiprocessing import
from multiprocessing.pool import Pool
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用https安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {'Connection': 'keep-alive',
          'Cache-Control': 'max-age=0',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Encoding': 'gzip, deflate, sdch',
          'Accept-Language': 'zh-CN,zh;q=0.8',
          }


class GetFreeProxy(object):

    def __init__(self):
        pass

    # @TODO gao ni ti qu
    def freeproxy1(self, proxy_number=100):

        url = "http://www.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=".format(
            proxy_number)

        html = self.get_page(url)
        for proxy in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html):
            yield proxy

    def freeproxy2(self):
        url = 'http://www.ip181.com/'
        html = self.get_page(url)
        soup = bs(html, 'html5lib')
        d = {}
        for i, v in enumerate(soup.find_all('tr')):
            if i != 0:
                tds = v.find_all('td')
                d['ip'] = tds[0].contents[0]
                d['port'] = tds[1].contents[0]
                yield d['ip'] + ':' + d['port']


    def get_page(self, url):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
            return '404'
        except requests.ConnectionError as e:
            print('Get Error', e.args)


def formatchecker(proxy):
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    return True if re.findall(verify_regex, proxy) else False


def proxychecker(proxy):
    if formatchecker(proxy):
        proxies = {"https": "https://{proxy}".format(proxy=proxy)}
        try:
            # 超过40秒的代理就不要了
            r = requests.get('https://www.baidu.com', proxies=proxies, timeout=20, verify=False)
            if r.status_code == 200:
                #logger.debug('%s is ok' % proxy)
                print(proxy, 'OK')
                return proxy
        except Exception as e:
            #print('Checker Error')
            pass
    print(proxy, '--')
    return


if __name__ == '__main__':
    import threading
    gg = GetFreeProxy()
    pool = Pool()

    for i in gg.freeproxy1():
        #print(proxychecker(i))
        pool.apply_async(proxychecker, args=(i, ))

    threads = []
    for i in gg.freeproxy1():
        t = threading.Thread(target=proxychecker, args=(i, ))
        threads.append(t)

    for i in range(len(threads)):
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()

    pool.close()
    pool.join()
    print('---END---')
