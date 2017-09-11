import json
import requests
from requests.exceptions import RequestException
import re



def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def create_file():
    with open('result2.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps('Blog Spider', ensure_ascii=False) + '\n')


def write_to_file(content):
    with open('result2.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def parse_one_page(html):
    pattern = re.compile('<section.*?description.*?>Abstract(.*?)</p>.*?</section>', re.S)
    items = re.findall(pattern, html)
    print(items)

    return items

def main(page):

    url = 'https://amberno1111.github.io/page/' + str(page) if page > 1 else 'https://amberno1111.github.io'
    html = get_one_page(url)
    #print(html)
    items = parse_one_page(html)
    for item in items:
        write_to_file(item)

if __name__ == '__main__':
    create_file()
    for i in range(5):
        main(i+1)
