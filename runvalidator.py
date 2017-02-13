#-*- coding: utf-8 -*-

import logging
import os
import sys
import time
import scrapydo
import utils

from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from ipproxytool.spiders.validator.douban import DoubanSpider
from ipproxytool.spiders.validator.assetstore import AssetStoreSpider
from ipproxytool.spiders.validator.gather import GatherSpider

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

    utils.make_dir('log')

    while True:
        utils.log('----------------validator start...-----------------------')
        items = scrapydo.run_spider(DoubanSpider)
        # items = scrapydo.run_spider(GatherSpider)
        # items = scrapydo.run_spider(AssetStoreSpider)
        utils.log('*************************validator waiting...*************************')
        time.sleep(60)
