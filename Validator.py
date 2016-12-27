# coding=utf-8

import Queue
import json
import time
import logging
import requests

from config import *
import mysql.connector
from SqlHelper import SqlHelper
from Proxy import Proxy


class Validator(object):
    def __init__(self, queue):
        self.queue = queue
        self.sql = SqlHelper()
        self.count = 0

        self.init()

    def init(self):
        # #读取之前的所有数据，存储到需要验证的队列
        # all_proxy = self.sql.select_all()
        # for row in all_proxy:
        #     proxy = Proxy()
        #     proxy.set_value(
        #             ip = row[0],
        #             port = row[1],
        #             country = row[2],
        #             anonymity = row[3],
        #             https = row[4],
        #             speed = row[5],
        #     )
        #
        #     self.queue.put(proxy)
        #
        # #清空之前所有的缓存代理
        # self.sql.clear_all()

        pass

    def run(self):
        while True:
            #阻塞，直到取到数据
            proxy = self.queue.get()
            logging.info('validator:' + str(proxy))
            
            if proxy.https == 'yes':
                continue
            
            proxies = {
                'http': 'http://%s:%s' % (proxy.ip, proxy.port)
            }
            
            ret = False
            
            #开始验证代理 ip 的有效性，目前只验证 http，暂时忽略 https
            try:
                start = time.time()
                r = requests.get(VALIDATOR_URL, proxies = proxies, timeout = 5)
                if r.ok and r.text.find(VALIDATOR_TEXT):
                    speed = time.time() - start
                    print('success validator:' + str(proxy))

                    if speed < 4:
                        ret = True
                        proxy.speed = str(speed)
                else:
                    print('code error validator:' + str(proxy))
            except:
                print('net except error validator:' + str(proxy))
                continue

            if ret:
                self.sql.insert_data(proxy)
    
    def write(self, filename, data):
        with open(filename, 'w') as f:
            f.write(data)
            f.close()
