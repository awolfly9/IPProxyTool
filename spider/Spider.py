# coding=utf-8

import logging
import time
import datetime
import requests
from utils import *
from config import *
from SqlHelper import SqlHelper


class Spider(object):
    def __init__(self, queue):
        self.queue = queue
        self.name = 'Spider'
        self.urls = []
        self.headers = {}
        self.timeout = 10
        self.sql = SqlHelper()

    def run(self):
        for i, url in enumerate(self.urls):
            try:
                r = requests.get(url, headers = self.headers, timeout = self.timeout)
                self.write(r.text.encode('utf-8'))
                self.parse_page(r)
            except Exception, e:
                log('spider run %s Exception:%s' % (self.name, str(e)), logging.WARNING)

    def parse_page(self, r):
        pass

    def add_proxy(self, proxy):
        #self.queue.put(proxy)

        command = get_insert_data_command(free_ipproxy_table)
        msg = (None, proxy.ip, proxy.port, proxy.country, proxy.anonymity, proxy.https, proxy.speed, None)

        self.sql.insert_data(command, msg)

    def write(self, data):
        with open('log/%s - %s.html' % (self.name, datetime.datetime.now().strftime('%Y-%m-%d %H:%m:%s:%f')), 'w') as f:
            f.write(data)
            f.close()
