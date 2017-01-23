# coding=utf-8

import logging
import time

from proxy import Proxy
from spider.usproxy import UsProxySpider
from spider.freeproxylists import FreeProxyListsSpider
from spider.gatherproxy import GatherproxySpider
from spider.sixsixip import SixSixIpSpider
from spider.kuaidaili import KuaiDaiLiSpider
from spider.peuland import PeulandSpider
from spider.xicidaili import XiCiDaiLiSpider

from utils import *
from sqlhelper import SqlHelper
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
        self.spiders.append(XiCiDaiLiSpider(self.queue))
        self.spiders.append(SixSixIpSpider(self.queue))
        # self.spiders.append(UsProxySpider(self.queue))
        # self.spiders.append(FreeProxyListsSpider(self.queue))
        # self.spiders.append(GatherproxySpider(self.queue))
        # self.spiders.append(KuaiDaiLiSpider(self.queue))
        # self.spiders.append(PeulandSpider(self.queue))

    def run(self):
        while (True):
            command = 'DELETE FROM {0} WHERE save_time < now() - 3600'.format(free_ipproxy_table)
            self.sql.execute(command)

            for spider in self.spiders:
                log('%s get proxy ip start' % spider.name)
                spider.run()

            log('Spider waiting...')
            time.sleep(WAIT_TIME)


if __name__ == '__main__':
    spider = RunSpider(None)
    spider.run()
