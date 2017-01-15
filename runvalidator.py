#-*- coding: utf-8 -*-
import logging
from scrapy import cmdline

if __name__ == '__main__':
    logging.basicConfig(
            filename = 'log/validator.log',
            format = '%(levelname)s %(asctime)s: %(message)s',
            level = logging.DEBUG
    )

    cmdline.execute('scrapy crawl validator'.split())