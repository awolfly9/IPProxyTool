# coding=utf-8

import logging
import time
import datetime
import requests
import sys

from utils import *
from config import *
from sqlhelper import SqlHelper
from scrapy.spiders import Spider, CrawlSpider
from scrapy.http import Request

reload(sys)
sys.setdefaultencoding('utf8')


class BaseSpider(Spider):
    name = 'basespider'

    def __init__(self, *a, **kw):
        super(BaseSpider, self).__init__(*a, **kw)

        self.urls = []
        self.headers = {}
        self.timeout = 10
        self.meta = {
            'download_timeout': self.timeout,
        }

        self.sql = SqlHelper()

        self.dir_log = 'log/proxy/%s' % self.name

    def init(self):
        make_dir(self.dir_log)

        command = get_create_table_command(free_ipproxy_table)
        self.sql.execute(command)

    def start_requests(self):
        for i, url in enumerate(self.urls):
            yield Request(
                    url = url,
                    headers = self.headers,
                    meta = self.meta,
                    dont_filter = True,
                    callback = self.parse_page,
                    errback = self.error_parse,
            )

    def parse_page(self, response):
        pass

    def error_parse(self, failure):
        request = failure.request
        pass

    def add_proxy(self, proxy):
        sql_insert_proxy(self.sql, free_ipproxy_table, proxy)

    def write(self, data):
        with open('%s/%s.html' % (
                self.dir_log, datetime.datetime.now().strftime('%Y-%m-%d %H:%m:%s:%f')), 'w') as f:
            f.write(data)
            f.close()
