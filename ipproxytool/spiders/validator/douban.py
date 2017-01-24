#-*- coding: utf-8 -*-

import copy
import time

from scrapy.http import Request
from scrapy.spiders import Spider, CrawlSpider
from sqlhelper import SqlHelper
from config import *
from utils import *
from scrapy.spidermiddlewares.httperror import HttpErrorMiddleware, HttpError
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
from validator import Validator


class DoubanSpider(Validator):
    name = 'douban'

    def __init__(self, name = None, **kwargs):
        super(DoubanSpider, self).__init__(name, **kwargs)

        self.timeout = 5

        self.init()

    def start_requests(self):
        count = get_table_length(self.sql, self.name)
        count_free = get_table_length(self.sql, free_ipproxy_table)

        for i in range(0, count + count_free):
            table = self.name if (i < count) else free_ipproxy_table

            proxy = get_proxy_info(self.sql, table, i)
            if proxy == None:
                continue

            url = 'https://movie.douban.com/subject/3434070/?from=subject-page'
            cur_time = time.time()
            yield Request(
                    url = url,
                    headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Connection': 'keep-alive',
                        'Host': 'movie.douban.com',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 '
                                      'Firefox/50.0',
                    },
                    meta = {
                        'cur_time': cur_time,
                        'download_timeout': self.timeout,
                        'proxy_info': proxy,
                        'table': table,
                        'id': proxy.get('id'),
                        'proxy': 'http://%s:%s' % (proxy.get('ip'), proxy.get('port')),
                    },
                    dont_filter = True,
                    callback = self.success_parse,
                    errback = self.error_parse,
            )

    def success_parse(self, response):
        self.log('success_parse proxy:%s' % str(response.meta.get('proxy')))

        filename = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S_%f')
        self.save_page(filename, response.body)

        if response.body.find('douban'):
            proxy = response.meta.get('proxy_info')
            speed = time.time() - response.meta.get('cur_time')
            table = response.meta.get('table')
            id = response.meta.get('id')

            self.log('speed:%s table:%s id:%s' % (speed, table, id))

            if table == self.name:
                if speed > self.timeout:
                    command = get_delete_data_command(table, id)
                    self.sql.execute(command)
                else:
                    command = get_update_data_command(table, id, speed)
                    self.sql.execute(command)
            else:
                if speed < self.timeout:
                    command = get_insert_data_command(self.name)
                    msg = (None, proxy.get('ip'), proxy.get('port'), proxy.get('country'), proxy.get('anonymity'),
                           proxy.get('https'), speed, proxy.get('source'), None)

                    self.sql.insert_data(command, msg)
