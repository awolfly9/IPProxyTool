#-*- coding: utf-8 -*-
import time

import datetime

import utils

from scrapy import Request
from scrapy.spiders import Spider
from config import free_ipproxy_table
from sqlhelper import SqlHelper


class Validator(Spider):
    name = 'base'

    def __init__(self, name = None, **kwargs):
        super(Validator, self).__init__(name, **kwargs)
        self.sql = SqlHelper()

        self.dir_log = 'log/validator/%s' % self.name
        self.timeout = 10

        self.urls = []
        self.headers = None
        self.success_mark = ''

    def init(self):
        utils.make_dir(self.dir_log)

        command = utils.get_create_table_command(self.name)
        self.sql.create_table(command)

    def start_requests(self):
        count = utils.get_table_length(self.sql, self.name)
        count_free = utils.get_table_length(self.sql, free_ipproxy_table)

        for i in range(0, count + count_free):
            table = self.name if (i < count) else free_ipproxy_table

            proxy = utils.get_proxy_info(self.sql, table, i)
            if proxy == None:
                continue

            for url in self.urls:
                cur_time = time.time()
                yield Request(
                        url = url,
                        headers = self.headers,
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
        self.log('name:%s success_parse proxy:%s' % (self.name, str(response.meta.get('proxy_info'))))

        filename = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S_%f')
        self.save_page(filename, response.body)

        if response.body.find(self.success_mark) or self.success_mark is '':
            proxy = response.meta.get('proxy_info')
            speed = time.time() - response.meta.get('cur_time')
            table = response.meta.get('table')
            id = response.meta.get('id')

            self.log('speed:%s table:%s id:%s' % (speed, table, id))

            if table == self.name:
                if speed > self.timeout:
                    command = utils.get_delete_data_command(table, id)
                    self.sql.execute(command)
                else:
                    command = utils.get_update_data_command(table, id, speed)
                    self.sql.execute(command)
            else:
                if speed < self.timeout:
                    command = utils.get_insert_data_command(self.name)
                    msg = (None, proxy.get('ip'), proxy.get('port'), proxy.get('country'), proxy.get('anonymity'),
                           proxy.get('https'), speed, proxy.get('source'), None)

                    self.sql.insert_data(command, msg)

    def error_parse(self, failure):
        self.log('error_parse value:%s' % failure.value)

        proxy = failure.request.meta.get('proxy_info')
        table = failure.request.meta.get('table')
        id = failure.request.meta.get('id')

        if table == self.name:
            command = utils.get_delete_data_command(table, id)
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

    def save_page(self, filename, data):
        with open('%s/%s.html' % (self.dir_log, filename), 'w') as f:
            f.write(data)
            f.close()
