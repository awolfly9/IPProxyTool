#-*- coding: utf-8 -*-

import logging
import os
import sys
import time
import scrapydo
import utils
import datetime

from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from ipproxytool.spiders.validator.douban import DoubanSpider
from ipproxytool.spiders.validator.assetstore import AssetStoreSpider
from ipproxytool.spiders.validator.gather import GatherSpider
from ipproxytool.spiders.validator.httpbin import HttpBinSpider

scrapydo.setup()

if __name__ == '__main__':
    os.chdir(sys.path[0])

    reload(sys)
    sys.setdefaultencoding('utf-8')

    if not os.path.exists('log'):
        os.makedirs('log')

    logging.basicConfig(
            filename = 'log/validator.log',
            format = '%(levelname)s %(asctime)s: %(message)s',
            level = logging.DEBUG
    )

    while True:
        utils.log('----------------validator start time:%s...-----------------------' %
                  datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S:%f'))

        items = scrapydo.run_spider(HttpBinSpider)

        utils.log('----------------validator finish:%s time:%s-----------------------' % (
            HttpBinSpider.name, datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S:%f')))
        time.sleep(10)

        items = scrapydo.run_spider(DoubanSpider)
        utils.log('----------------validator finish:%s time:%s-----------------------' % (
            DoubanSpider.name, datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S:%f')))

        # items = scrapydo.run_spider(GatherSpider)
        # items = scrapydo.run_spider(AssetStoreSpider)

        utils.log('*************************validator waiting time:%s...*************************' %
                  datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S:%f'))

        time.sleep(60)
