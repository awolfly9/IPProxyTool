# coding=utf-8

import logging
import time

from Proxy import Proxy
from UsProxySpider import UsProxySpider
from FreeProxyListsSpider import FreeProxyListsSpider
from GatherproxySpider import GatherproxySpider
from SixSixIpSpider import SixSixIpSpider
from KuaiDaiLiSpider import KuaiDaiLiSpider
from PeulandSpider import PeulandSpider
from utils import *
from SqlHelper import SqlHelper
from config import *


class RunSpider(object):
    def __init__(self, queue):
        self.spiders = []
        self.queue = queue
        self.sql = SqlHelper()
        self.register_spider()
        self.init()

    def init(self):
        self.create_table()

    def create_table(self):
        command = get_create_table_command(free_ipproxy_table)

        self.sql.create_table(command)

    def register_spider(self):
        self.spiders.append(UsProxySpider(self.queue))
        self.spiders.append(FreeProxyListsSpider(self.queue))
        self.spiders.append(GatherproxySpider(self.queue))
        self.spiders.append(SixSixIpSpider(self.queue))
        self.spiders.append(KuaiDaiLiSpider(self.queue))
        self.spiders.append(PeulandSpider(self.queue))

    def run(self):
        while (True):
            for spider in self.spiders:
                log('%s get proxy ip start' % spider.name)
                spider.run()

            log('Spider waiting...')
            time.sleep(WAIT_TIME)


if __name__ == '__main__':
    spider = RunSpider(None)
    spider.run()
