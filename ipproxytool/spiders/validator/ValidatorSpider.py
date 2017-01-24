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


class ValidatorSpider(Spider):
    name = 'validator'

    def __init__(self, name = None, **kwargs):
        super(ValidatorSpider, self).__init__(name, **kwargs)
        self.sql = SqlHelper()

        self.validator_info = copy.copy(validator_ipproxy)
        self.init()

    def init(self):
        for i, item in enumerate(self.validator_info):
            table = item.get('table')

            command = get_create_table_command(table)
            self.sql.create_table(command)

            self.get_table_length(table)

        self.get_table_length(free_ipproxy_table)

    def start_requests(self):
        count = self.get_table_length(free_ipproxy_table)

        for i in range(1, count):
            proxy = self.get_proxy_info(free_ipproxy_table, i)
            if proxy == None:
                continue

            for item in self.validator_info:
                url = item.get('url')
                self.log('start_requests url:%s' % url)
                self.log('\n%s\n' % item.get('headers'))

                cur_time = time.time()

                yield Request(
                        url = url,
                        headers = json.loads(item.get('headers')),
                        meta = {
                            'validator': item,
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
        self.log('success_parse validator:%s' % response.meta['validator'])
        v = response.meta.get('validator')

        if response.body.find(v.get('success')):
            table_name = v.get('table')

            proxy = response.meta.get('proxy_info')

            command = get_insert_data_command(table_name)

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
            self.logger.error('TimeoutError on meta:%s', request.meta['validator'])

    def get_table_length(self, table_name):
        command = ('select id from {} order by id desc limit 1'.format(table_name))
        results = self.sql.query_one(command)
        if results != None and len(results) > 0:
            id = results[0]
            self.log('id:%s' % id)
            return int(id)
        return 0

    def get_proxy_info(self, table_name, id):
        command = ('select * from {0} where id={1}'.format(table_name, id))
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
                'save_time': result[7],
            }
            return data
        return None
