#-*- coding: utf-8 -*-

import time
import datetime
import utils
import config

from scrapy import Request
from scrapy.spiders import Spider
from scrapy.utils.project import get_project_settings
from sqlhelper import SqlHelper


class Validator(Spider):
    name = 'base'
    concurrent_requests = 16
    retry_enabled = False

    def __init__(self, name = None, **kwargs):
        super(Validator, self).__init__(name, **kwargs)
        self.sql = SqlHelper()

        self.dir_log = 'log/validator/%s' % self.name
        self.timeout = 10

        self.urls = []
        self.headers = None
        self.success_mark = ''
        self.is_record_web_page = False

    def init(self):
        utils.make_dir(self.dir_log)

        command = utils.get_create_table_command(self.name)
        self.sql.create_table(command)

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(cls.custom_settings or {
            'CONCURRENT_REQUESTS': cls.concurrent_requests,
            'RETRY_ENABLED': cls.retry_enabled
        },
                         priority = 'spider')

    def start_requests(self):
        count = utils.get_table_length(self.sql, self.name)
        count_free = utils.get_table_length(self.sql, config.httpbin_table)

        for i in range(0, count + count_free):
            table = self.name if (i < count) else config.httpbin_table

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
        utils.log('name:%s success_parse proxy:%s meta:%s' % (
            self.name, str(response.meta.get('proxy_info')), str(response.meta)))

        filename = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S_%f')
        self.save_page(filename, response.body)

        if response.body.find(self.success_mark) or self.success_mark is '':
            proxy = response.meta.get('proxy_info')
            speed = time.time() - response.meta.get('cur_time')
            table = response.meta.get('table')
            id = response.meta.get('id')

            utils.log('speed:%s table:%s id:%s' % (speed, table, id))

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
        request = failure.request
        utils.log('error_parse value:%s url:%s meta:%s' % (failure.value, request.url, request.meta))

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
            # utils.log('request meta:%s' % str(request))
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
        if self.is_record_web_page:
            with open('%s/%s.html' % (self.dir_log, filename), 'w') as f:
                f.write(data)
                f.close()
