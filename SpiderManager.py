# coding=utf-8

import logging
import time

from Proxy import Proxy
from Spiders.UsProxySpider import UsProxySpider
from Spiders.FreeProxyListsSpider import FreeProxyListsSpider
from Spiders.GatherproxySpider import GatherproxySpider
from Spiders.SixSixIpSpider import SixSixIpSpider
from SqlHelper import SqlHelper
from config import WAIT_TIME


class SpiderManager(object):
    def __init__(self, queue):
        self.spiders = []
        self.queue = queue
        self.sql = SqlHelper()
        self.register_spider()

    def init(self):
        #读取之前的所有数据，存储到需要验证的队列
        all_proxy = self.sql.select_all()
        for row in all_proxy:
            proxy = Proxy()
            proxy.set_value(
                    ip = row[0],
                    port = row[1],
                    country = row[2],
                    anonymity = row[3],
                    https = row[4],
                    speed = row[5],
            )

            self.queue.put(proxy)

        #清空之前所有的缓存代理
        self.sql.clear_all()

    def register_spider(self):
        self.spiders.append(UsProxySpider(self.queue))
        self.spiders.append(FreeProxyListsSpider(self.queue))
        self.spiders.append(GatherproxySpider(self.queue))
        self.spiders.append(SixSixIpSpider(self.queue))

    def run(self):
        while (True):
            self.init()
            for spider in self.spiders:
                spider.run()

            logging.info('Spider waiting...')
            print('Spider waiting...')
            time.sleep(WAIT_TIME)
