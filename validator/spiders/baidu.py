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

from basevalidator import BaseValidator


class BaiduSpider(BaseValidator):
    name = 'baidu'

    def __init__(self, name = None, **kwargs):
        super(BaiduSpider, self).__init__(name, **kwargs)

        self.dir_log = 'log/validator/baidu'
        self.table_name = 'baidu'
        self.init()

    def init(self):
        make_dir(self.dir_log)

        command = get_create_table_command(self.table_name)
        self.sql.create_table(command)

    def start_requests(self):
        count = self.get_table_length(free_ipproxy_table)

        for i in range(1, count):
            proxy = self.get_proxy_info(free_ipproxy_table, i)
            if proxy == None:
                continue

            url = 'https://www.baidu.com/'
            cur_time = time.time()
            yield Request(
                    url = url,
                    headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Cache-Control': 'max-age=0',
                        'Connection': 'keep-alive',
                        'Host': 'www.baidu.com',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 '
                                      'Firefox/50.0',
                    },
                    meta = {
                        'cur_time': cur_time,
                        'download_timeout': 10,
                        'proxy_info': proxy,
                        'id': proxy.get('id'),
                        'proxy': 'http://%s:%s' % (proxy.get('ip'), proxy.get('port'))
                    },
                    dont_filter = True,
                    callback = self.success_parse,
                    errback = self.error_parse,
            )

    def success_parse(self, response):
        self.log('success_parse url:%s' % response.url)

        filename = datetime.datetime.now().strftime('%Y-%m-%d %H:%m:%s:%f')
        self.save_page(filename, response.body)

        if response.body.find('baidu'):
            proxy = response.meta.get('proxy_info')

            command = get_insert_data_command(self.table_name)

            speed = time.time() - response.meta.get('cur_time')

            msg = (
                None, proxy.get('ip'), proxy.get('port'), proxy.get('country'), proxy.get('anonymity'),
                proxy.get('https'),
                speed, None)

            self.sql.insert_data(command, msg)

    def error_parse(self, failure):
        self.log('error_parse')
        self.log('error_parse value:%s' % failure.value)

        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        self.logger.error(repr(failure))

        #if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on url:%s', request.url)

    def get_table_length(self, table_name):
        command = ('SELECT COUNT(*) from {}'.format(table_name))
        self.sql.execute(command)
        (count,) = self.sql.cursor.fetchone()
        self.log('get_table_length results:%s' % str(count))
        return count

    def get_proxy_info(self, table_name, id):
        command = ('select * from {0} limit {1},1;'.format(table_name, id))
        result = self.sql.query_one(command)
        if result != None:
            data = {
                'id': result[0],
                'ip': result[1],
                'port': result[2],
                'country': result[3],
                'anonymity': result[4],
                'https': result[5],
                'speed': result[6],
                'source': result[7],
                'save_time': result[8],
            }
            return data
        return None

    def save_page(self, filename, data):
        with open('%s/%s.html' % (self.dir_log, filename), 'w') as f:
            f.write(data)
            f.close()
