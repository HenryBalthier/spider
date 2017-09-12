# -*- coding: utf-8 -*-
# !/usr/bin/env python
from proj1.multwork import *


class Get_Page(object):

    def __init__(self):
        self.mult = MultTheading()
        self.proxy = next(self.mult)

    def get_page(self, url, proxies=None, headers=None):
        if proxies is not None:
            proxies = self.proxy
        try:
            responce = requests.get(url, headers=headers, proxies=proxies)
            if responce.status_code == 200:
                return responce

            print(self.proxy, '404')
            self.proxy = next(self.mult)
            return '404'
        except requests.ConnectionError as e:
            print('Get Error', e)

if __name__ == '__main__':
    get = Get_Page()
    print(get.get_page('https://www.baidu.com', proxies=True))
