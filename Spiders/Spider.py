# coding=utf-8
import logging
import time

import datetime
import requests


class Spider(object):
    def __init__(self, queue):
        self.queue = queue
        self.name = 'Spider'
        self.urls = []
        self.headers = {}

    def run(self):
        for i, url in enumerate(self.urls):
            try:
                r = requests.get(url, headers = self.headers)
                self.write(r.text.encode('utf-8'))
                self.parse_page(r)
            except Exception, e:
                logging.warning('FreeProxyListsSpider Exception:%s' % str(e))
                print('FreeProxyListsSpider Exception:%s' % str(e))

    def parse_page(self, r):
        pass

    def add_proxy(self, proxy):
        self.queue.put(proxy)

    def write(self, data):
        #with open('log/%s - %s.html' % (self.name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), 'w') as f:
        with open('log/%s - %s.html' % (self.name, datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')), 'w') as f:
            f.write(data)
            f.close()
