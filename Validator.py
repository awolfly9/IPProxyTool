# coding=utf-8

import Queue
import json
import time
import logging

import datetime
import requests

from config import *
from SqlHelper import SqlHelper
from Proxy import Proxy


class Validator(object):
    def __init__(self, queue):
        self.queue = queue
        self.sql = SqlHelper()
        print('Validator sql:%s' % self.sql)
        self.count = 0

        self.headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.assetstore.unity3d.com',
            'Referer': 'https://www.assetstore.unity3d.com/en/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 '
                          'Firefox/50.0',
            'X-Kharma-Version': '0',
            'X-Requested-With': 'UnityAssetStore',
            'X-Unity-Session': '26c4202eb475d02864b40827dfff11a14657aa41',
        }

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
                'http': 'http://%s:%s' % (proxy.ip, proxy.port),
                #'https': 'http://%s:%s' % (proxy.ip, proxy.port)
            }
            
            ret = False
            
            # #开始验证代理 ip 的有效性，目前只验证 http，暂时忽略 https
            # try:
            #     headers = {
            #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            #         'Accept-Encoding': 'gzip, deflate',
            #         'Accept-Language': 'en-US,en;q=0.5',
            #         'Connection': 'keep-alive',
            #         'Host': 'ip.chinaz.com',
            #         'Upgrade-Insecure-Requests': '1',
            #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
            #     }
            #     r = requests.get('http://ip.chinaz.com/', proxies = proxies, headers = headers, timeout = 10)
            #     self.write('log/ip_chinaz_%s.html' % time.strftime('%y-%m-%d %H:%M:%S', time.localtime()), r.text)
            #
            #     if proxy.ip not in r.text:
            #         print('ip error:%s' % str(proxies))
            #         continue
            # except Exception, e:
            #     print('net ip chinaz error msg:%s' % e)
            #     continue

            # try:
            #     r = requests.get('http://ip-check.info/?lang=en', proxies = proxies, timeout = 10)
            #     self.write('log/ip_chinaz_%s.html' % time.strftime('%y-%m-%d %H:%M%S', time.localtime()), r.text)
            #
            #     if proxy.ip not in r.text:
            #         print('ip error:%s' % str(proxies))
            #         continue
            # except Exception, e:
            #     print('net ip chinaz error msg:%s' % e)
            #     continue

            try:
                r = requests.get('https://www.baidu.com/', proxies = proxies, timeout = 10)
                self.write('log/baidu_%s.html' % time.strftime('%Y-%m-%d %H:%M%S:%F', time.localtime()), r.text)

                if 'www.baidu.com' not in r.text:
                    print('ip error:%s' % str(proxies))
                    continue
            except Exception, e:
                print('net ip baidu error msg:%s' % e)
                continue

            try:
                r = requests.get('https://www.douban.com/', proxies = proxies, timeout = 10)
                self.write('log/douban - %s.html' % time.strftime('%Y-%m-%d %H:%M%S:%F', time.localtime()), r.text)

                if 'https://www.douban.com' not in r.text:
                    print('ip error:%s' % str(proxies))
                    continue
            except Exception, e:
                print('net ip steam error msg:%s' % e)
                continue

            # try:
            #     r = requests.get('http://store.steampowered.com/', proxies = proxies, timeout = 10)
            #     self.write('log/steam - %s.html' % time.strftime('%Y-%m-%d %H:%M%S:%F', time.localtime()), r.text)
            #
            #     if 'http://store.steampowered.com' not in r.text:
            #         print('ip error:%s' % str(proxies))
            #         continue
            # except Exception, e:
            #     print('net ip steam error msg:%s' % e)
            #     continue

            # try:
            #     start = time.time()
            #     r = requests.get(VALIDATOR_URL, headers = self.headers, proxies = proxies, timeout = 5)
            #     self.write('log/asset_store_%s.html' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), r.text)
            #
            #     if r.ok and r.text.find(VALIDATOR_TEXT):
            #         speed = time.time() - start
            #         print('success validator:' + str(proxy))
            #
            #         if speed < 4:
            #             ret = True
            #             proxy.speed = str(speed)
            #     else:
            #         print('code error validator:' + str(proxy))
            # except Exception, e:
            #     print('net except error validator:%s  error msg:%s' % (str(proxy), e))
            #     continue

            if ret:
                self.sql.insert_data(proxy)
    
    def write(self, filename, data):
        with open(filename, 'w') as f:
            f.write(data)
            f.close()
