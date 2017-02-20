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

scrapydo.setup()

if __name__ == '__main__':

    os.chdir(sys.path[0])

    reload(sys)
    sys.setdefaultencoding('utf-8')

    if not os.path.exists('log'):
        os.makedirs('log')

    logging.basicConfig(
            filename = 'log/proxy.log',
            format = '%(levelname)s %(asctime)s: %(message)s',
            level = logging.DEBUG
    )
    sql = SqlHelper()

    while True:
        utils.log('*******************run spider start...*******************')

        command = 'DELETE FROM {0} WHERE save_time < now() - {1}'.format(config.free_ipproxy_table, 1800)
        sql.execute(command)

        items = scrapydo.run_spider(XiCiDaiLiSpider)
        items = scrapydo.run_spider(SixSixIpSpider)
        items = scrapydo.run_spider(IpOneEightOneSpider)
        items = scrapydo.run_spider(KuaiDaiLiSpider)
        items = scrapydo.run_spider(GatherproxySpider)
        items = scrapydo.run_spider(HidemySpider)
        items = scrapydo.run_spider(ProxylistplusSpider)
        items = scrapydo.run_spider(FreeProxyListsSpider)
        items = scrapydo.run_spider(PeulandSpider)
        items = scrapydo.run_spider(UsProxySpider)

        utils.log('*******************run spider waiting...*******************')
        time.sleep(300)
