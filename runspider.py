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

scrapydo.setup()

if __name__ == '__main__':

    os.chdir(sys.path[0])

    reload(sys)
    sys.setdefaultencoding('utf-8')

    utils.make_dir('log')

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

        utils.log('*******************run spider waiting...*******************')
        time.sleep(300)
