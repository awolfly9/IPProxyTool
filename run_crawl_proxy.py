# -*- coding: utf-8 -*-

import logging
import os
import sys
import scrapydo
import time
import utils
import config

from sql import SqlManager
from crawler.spiders.proxy.xicidaili import XiCiDaiLiSpider
from crawler.spiders.proxy.sixsixip import SixSixIpSpider
from crawler.spiders.proxy.ip181 import IpOneEightOneSpider
from crawler.spiders.proxy.kuaidaili import KuaiDaiLiSpider
from crawler.spiders.proxy.gatherproxy import GatherproxySpider
from crawler.spiders.proxy.hidemy import HidemySpider
from crawler.spiders.proxy.proxylistplus import ProxylistplusSpider
from crawler.spiders.proxy.freeproxylists import FreeProxyListsSpider
from crawler.spiders.proxy.usproxy import UsProxySpider
from crawler.spiders.proxy.proxydb import ProxyDBSpider


scrapydo.setup()

if __name__ == '__main__':
    os.chdir(sys.path[0])

    if not os.path.exists('log'):
        os.makedirs('log')

    logging.basicConfig(
        filename = 'log/crawl_proxy.log',
        format = '%(levelname)s %(asctime)s: %(message)s',
        level = logging.DEBUG
    )
    sql = SqlManager()

    spiders = [
        XiCiDaiLiSpider,
        SixSixIpSpider,
        IpOneEightOneSpider,
        KuaiDaiLiSpider,  # 在访问前加了一个 js ，反爬
        GatherproxySpider,
       # HidemySpider,  已失效
        ProxylistplusSpider,
        FreeProxyListsSpider,
        # PeulandSpider,  # 目标站点失效
        UsProxySpider,
        ProxyDBSpider,
    ]
    while True:
        utils.log('*******************run spider start...*******************')
        #sql.delete_old(config.free_ipproxy_table, 0.5)
        try:
            for spider in spiders:
                scrapydo.run_spider(spider_cls = spider)
        except Exception as e:
            utils.log('[Error]# spider goes wroing.Return Message: {}'.format(str(e)))
     
        utils.log('*******************run spider waiting...*******************')
        time.sleep(1200)
