# -*- coding: utf-8 -*-

import os
import logging
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


def runspider(name):
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log/%s.log' % name,
        format='%(levelname)s %(asctime)s: %(message)s',
        level=logging.DEBUG
    )
    process = CrawlerProcess(get_project_settings())
    try:
        logging.info('runspider start spider:%s' % name)
        process.crawl(name)
        process.start()
    except Exception as e:
        logging.exception('runspider spider:%s exception:%s' % (name, e))

    logging.debug('finish this spider:%s\n\n' % name)


if __name__ == '__main__':
    try:
        name = sys.argv[1] or 'base'
        runspider(name)
    except Exception as e:
        logging.exception('run_spider main exception msg:%s' % e)
