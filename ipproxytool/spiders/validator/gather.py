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


class GatherSpider(Validator):
    name = 'gather'

    def __init__(self, name = None, **kwargs):
        super(GatherSpider, self).__init__(name, **kwargs)

        self.dir_log = 'log/validator/gather'
        self.table_name = 'gather'
        self.timeout = 10
        self.urls = [
            # 'http://gatherproxy.com/proxylist/anonymity/?t=Anonymous',
            'http://gatherproxy.com/proxylist/country/?c=China'
        ]

        self.init()

    def start_requests(self):
        count = get_table_length(self.sql, self.table_name)
        count_free = get_table_length(self.sql, free_ipproxy_table)

        for i in range(0, count + count_free):
            table = self.table_name if (i < count) else free_ipproxy_table

            proxy = get_proxy_info(self.sql, table, i)
            if proxy == None:
                continue

            for url in self.urls:
                cur_time = time.time()
                yield Request(
                        url = url,
                        headers = {
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Encoding': 'gzip, deflate',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Connection': 'keep-alive',
                            'Host': 'gatherproxy.com',
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

        filename = datetime.datetime.now().strftime('%Y-%m-%d %H:%m:%s:%f')
        self.save_page(filename, response.body)

        proxy = response.meta.get('proxy_info')
        speed = time.time() - response.meta.get('cur_time')
        table = response.meta.get('table')
        id = response.meta.get('id')

        if table == self.table_name:
            if speed > self.timeout:
                command = get_delete_data_command(table, id)
                self.sql.execute(command)
            else:
                command = get_update_data_command(table, id, speed)
                self.sql.execute(command)
        else:
            if speed < self.timeout:
                command = get_insert_data_command(self.table_name)
                msg = (None, proxy.get('ip'), proxy.get('port'), proxy.get('country'), proxy.get('anonymity'),
                       proxy.get('https'), speed, proxy.get('source'), None)

                self.sql.insert_data(command, msg)

    def error_parse(self, failure):
        self.log('error_parse')
        self.log('error_parse value:%s' % failure.value)

        proxy = failure.request.meta.get('proxy_info')
        table = failure.request.meta.get('table')
        id = failure.request.meta.get('id')

        if table == self.table_name:
            command = get_delete_data_command(table, id)
            self.sql.execute(command)
        else:
            # TODO... 如果 ip 验证失败应该针对特定的错误类型，进行处理
            pass

            #
            # request = failure.request.meta
            # self.log('request meta:%s' % str(request))
            #
            # # log all errback failures,
            # # in case you want to do something special for some errors,
            # # you may need the failure's type
            # self.logger.error(repr(failure))
            #
            # #if isinstance(failure.value, HttpError):
            # if failure.check(HttpError):
            #     # you can get the response
            #     response = failure.value.response
            #     self.logger.error('HttpError on %s', response.url)
            #
            # #elif isinstance(failure.value, DNSLookupError):
            # elif failure.check(DNSLookupError):
            #     # this is the original request
            #     request = failure.request
            #     self.logger.error('DNSLookupError on %s', request.url)
            #
            # #elif isinstance(failure.value, TimeoutError):
            # elif failure.check(TimeoutError):
            #     request = failure.request
            #     self.logger.error('TimeoutError on url:%s', request.url)
