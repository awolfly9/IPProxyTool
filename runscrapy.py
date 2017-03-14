#-*- coding: utf-8 -*-

import os
import logging
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


def runscrapy(name):
    configure_logging(install_root_handler = False)
    logging.basicConfig(
            filename = 'log/%s.log' % name,
            format = '%(levelname)s %(asctime)s: %(message)s',
            level = logging.DEBUG
    )
    process = CrawlerProcess(get_project_settings())
    try:
        logging.info('runscrapy start spider:%s' % name)
        process.crawl(name)
        process.start()
    except Exception, e:
        logging.error('runscrapy spider:%s exception:%s' % (name, e))
        pass

    logging.info('finish this spider:%s\n\n' % name)


if __name__ == '__main__':
    name = sys.argv[1] or 'base'
    print('name:%s' % name)
    print ('project dir:%s' % os.getcwd())

    runscrapy(name)
