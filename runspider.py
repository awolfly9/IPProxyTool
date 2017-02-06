#-*- coding: utf-8 -*-

import logging
import os
import sys
import scrapydo
import time

from sqlhelper import SqlHelper
from ipproxytool.spiders.proxy.xicidaili import XiCiDaiLiSpider
from ipproxytool.spiders.proxy.sixsixip import SixSixIpSpider
from ipproxytool.spiders.proxy.ip181 import IpOneEightOneSpider
from ipproxytool.spiders.proxy.kuaidaili import KuaiDaiLiSpider
from ipproxytool.spiders.proxy.gatherproxy import GatherproxySpider
from config import free_ipproxy_table

scrapydo.setup()

if __name__ == '__main__':

    os.chdir(sys.path[0])

    reload(sys)
    sys.setdefaultencoding('utf-8')

    logging.basicConfig(
            filename = 'log/proxy.log',
            format = '%(levelname)s %(asctime)s: %(message)s',
            level = logging.DEBUG
    )
    sql = SqlHelper()

    while True:
        print('*******************run spider start...*******************')

        command = 'delete from {0} where `save_time` < now() - {1};'.format(free_ipproxy_table, 3600)
        sql.execute(command)

        items = scrapydo.run_spider(XiCiDaiLiSpider)
        items = scrapydo.run_spider(SixSixIpSpider)
        items = scrapydo.run_spider(IpOneEightOneSpider)
        items = scrapydo.run_spider(KuaiDaiLiSpider)
        items = scrapydo.run_spider(GatherproxySpider)

        print('*******************run spider waiting...*******************')
        time.sleep(300)
