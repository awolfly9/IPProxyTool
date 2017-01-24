#-*- coding: utf-8 -*-

import logging
import os

import sys
import scrapydo
import time

scrapydo.setup()

from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from ipproxytool.spiders.proxy.xicidaili import XiCiDaiLiSpider
from ipproxytool.spiders.proxy.sixsixip import SixSixIpSpider
from ipproxytool.spiders.proxy.ip181 import IpOneEightOneSpider
from ipproxytool.spiders.proxy.kuaidaili import KuaiDaiLiSpider
from ipproxytool.spiders.proxy.gatherproxy import GatherproxySpider

if __name__ == '__main__':

    os.chdir(sys.path[0])

    reload(sys)
    sys.setdefaultencoding('utf-8')

    logging.basicConfig(
            filename = 'log/proxy.log',
            format = '%(levelname)s %(asctime)s: %(message)s',
            level = logging.DEBUG
    )

    while True:
        print('*******************run spider start...*******************')
        # process = CrawlerProcess()
        # process.crawl(XiCiDaiLiSpider)
        # process.crawl(SixSixIpSpider)
        # process.start()  # the script will block here until all crawling jobs are finished
        #
        items = scrapydo.run_spider(XiCiDaiLiSpider)
        items = scrapydo.run_spider(SixSixIpSpider)
        items = scrapydo.run_spider(IpOneEightOneSpider)
        items = scrapydo.run_spider(KuaiDaiLiSpider)
        items = scrapydo.run_spider(GatherproxySpider)


        print('*******************run spider waiting...*******************')
        # scrapydo.setup()
        time.sleep(300)
