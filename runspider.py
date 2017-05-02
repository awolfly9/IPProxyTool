#-*- coding: utf-8 -*-

import logging
import os
import sys
import scrapydo
import time
import utils
import config

from sqlhelper import SqlHelper
from ipproxytool.spiders.proxy.xicidaili import XiCiDaiLiSpider
from ipproxytool.spiders.proxy.sixsixip import SixSixIpSpider
from ipproxytool.spiders.proxy.ip181 import IpOneEightOneSpider
from ipproxytool.spiders.proxy.kuaidaili import KuaiDaiLiSpider
from ipproxytool.spiders.proxy.gatherproxy import GatherproxySpider
from ipproxytool.spiders.proxy.hidemy import HidemySpider
from ipproxytool.spiders.proxy.proxylistplus import ProxylistplusSpider
from ipproxytool.spiders.proxy.freeproxylists import FreeProxyListsSpider
from ipproxytool.spiders.proxy.peuland import PeulandSpider
from ipproxytool.spiders.proxy.usproxy import UsProxySpider
from ipproxytool.spiders.proxy.proxydb import ProxyDBSpider
from ipproxytool.spiders.proxy.proxyrox import ProxyRoxSpider

scrapydo.setup()

if __name__ == '__main__':
    os.chdir(sys.path[0])

    reload(sys)
    sys.setdefaultencoding('utf-8')

    if not os.path.exists('log'):
        os.makedirs('log')

    logging.basicConfig(
            filename = 'log/spider.log',
            format = '%(levelname)s %(asctime)s: %(message)s',
            level = logging.DEBUG
    )

    sql = SqlHelper()

    spiders = [
        XiCiDaiLiSpider,
        SixSixIpSpider,
        IpOneEightOneSpider,
        KuaiDaiLiSpider,  # 在访问前加了一个 js ，反爬
        GatherproxySpider,
        HidemySpider,
        ProxylistplusSpider,
        FreeProxyListsSpider,
        # PeulandSpider,  # 目标站点失效
        UsProxySpider,
        ProxyDBSpider,
        ProxyRoxSpider,
    ]

    while True:
        utils.log('*******************run spider start...*******************')

        command = "DELETE FROM {table} where save_time < SUBDATE(NOW(), INTERVAL 0.5 DAY)".format(
                table = config.free_ipproxy_table)
        sql.execute(command)

        for spider in spiders:
            scrapydo.run_spider(spider)

        utils.log('*******************run spider waiting...*******************')
        time.sleep(1200)
