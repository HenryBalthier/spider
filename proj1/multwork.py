
from proj1.proxygetter import *
#from proj1.dataspider import *

def MultProcessing():
    from multiprocessing.pool import Pool

    gg = GetFreeProxy()
    pool = Pool()
    queue = []

    for i in gg.freeproxy2():
        pool.apply_async(proxychecker, args=(i, queue))

    pool.close()
    pool.join()

    print(queue)


def MultTheading():
    import threading

    gg = GetFreeProxy()
    threads = []
    queue = []

    for i in gg.freeproxy2():
        t = threading.Thread(target=proxychecker, args=(i, queue))
        threads.append(t)
        t.start()

    for i in range(len(threads)):
        threads[i].join()

    print(queue)

    for i in queue:
        res = proxychecker(i)
        if res:
            proxies = {"https": "https://{proxy}".format(proxy=res), "http": "http://{proxy}".format(proxy=res)}
            yield proxies

if __name__ == '__main__':
    for i in MultTheading():
        print(i)

    print('---END---')