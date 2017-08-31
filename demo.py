import requests
import selenium
from selenium import webdriver
import aiohttp
import lxml
import gerapy
from urllib import request, parse
import re


def urltest():
    response = request.urlopen('https://www.python.org')
    print(response.read().decode('utf-8'))


def requesttest():
    req = request.Request('https://www.python.org')
    response = request.urlopen(req)
    print(response.read().decode('utf-8'))


def reqtest2():
    url = 'http://httpbin.org/post'
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        'Host': 'httpbin.org'
    }
    dict = {
        'name': 'Germey'
    }
    data = bytes(parse.urlencode(dict), encoding='utf8')
    req = request.Request(url=url, data=data, headers=headers, method='POST')
    response = request.urlopen(req)
    print(response.read().decode('utf-8'))


def reqs():
    r = requests.get('https://www.baidu.com/')
    print(type(r))
    print(r.status_code)
    print(type(r.text))
    print(r.text)
    print(r.cookies)


def reqs2():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    r = requests.get("https://www.zhihu.com/explore", headers=headers)
    pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
    titles = re.findall(pattern, r.text)
    print(titles)




if __name__ == '__main__':
    print('Hello World\n')
    reqs2()
