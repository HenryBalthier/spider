import os
import multiprocessing
from multiprocessing.pool import Pool
import requests
from urllib.parse import urlencode
from hashlib import md5


def get_page(offset):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None


def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_detail')


            for image in images:
                yield {
                    'image': image.get('url'),
                    'title': title
                }
            print('_______', multiprocessing.current_process())
    '''
            print('_______', multiprocessing.current_process(), images)
            if images:
                return title, images
            else:
                return None, None
    else:
        return None, None
    '''


def save_image(item):
    file_name = './images/' + item.get('title')
    if not os.path.exists(file_name):
        os.mkdir(file_name)
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(file_name, md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
        else:
            assert AssertionError
    except requests.ConnectionError:
        print('Failed to Save Image')


def main(offset):
    json = get_page(offset)

    for item in get_images(json):
        print(item)
        save_image(item)
    '''
    print('offset = ', offset)
    title, images = get_images(json)
    if images:
        for image in images:
            item = {
                    'image': image.get('url'),
                    'title': title
            }
            print(item)
            save_image(item)
    '''
GROUP_START = 1
GROUP_END = 2

if __name__ == '__main__':
    pool = Pool()
    lst = []

    for x in range(GROUP_START, GROUP_END + 1):
        res = pool.apply_async(main, args=(x * 20, ))
        lst.append(res)
    #groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    #pool.map(main, groups)

    for i in lst:
        print('waiting')
        i.get()


    pool.close()
    pool.join()
    print("***   END   ***")
