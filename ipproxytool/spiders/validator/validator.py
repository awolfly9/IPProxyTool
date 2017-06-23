#-*- coding: utf-8 -*-
import random
import time
import datetime
import utils
import config

from scrapy import Request
from scrapy.spiders import Spider
from sql import SqlManager


class Validator(Spider):
    name = 'base'
    concurrent_requests = 16
    retry_enabled = False

    def __init__(self, name = None, **kwargs):
        super(Validator, self).__init__(name, **kwargs)

        self.urls = []
        self.headers = None
        self.success_mark = ''
        self.timeout = 10
        self.is_record_web_page = False

        self.sql = SqlManager()

    def init(self):
        self.dir_log = 'log/validator/%s' % self.name
        utils.make_dir(self.dir_log)

        self.sql.init_proxy_table(self.name)

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(cls.custom_settings or {
            'CONCURRENT_REQUESTS': cls.concurrent_requests,
            'RETRY_ENABLED': cls.retry_enabled,
        },
                         priority = 'spider')

    def start_requests(self):
        count = self.sql.get_proxy_count(self.name)
        count_free = self.sql.get_proxy_count(config.httpbin_table)

        ids = self.sql.get_proxy_ids(self.name)
        ids_httpbin = self.sql.get_proxy_ids(config.httpbin_table)

        for i in range(0, count + count_free):
            table = self.name if (i < count) else config.httpbin_table
            id = ids[i] if i < count else ids_httpbin[i - len(ids)]

            proxy = self.sql.get_proxy_with_id(table, id)
            if proxy == None:
                continue

            url = random.choice(self.urls)
            cur_time = time.time()
            yield Request(
                    url = url,
                    headers = self.headers,
                    meta = {
                        'cur_time': cur_time,
                        'download_timeout': self.timeout,
                        'proxy_info': proxy,
                        'table': table,
                        'proxy': 'http://%s:%s' % (proxy.ip, proxy.port),
                    },
                    dont_filter = True,
                    callback = self.success_parse,
                    errback = self.error_parse,
            )

    def success_parse(self, response):
        proxy = response.meta.get('proxy_info')
        table = response.meta.get('table')

        self.save_page(proxy.ip, response.body)
        self.log('success_parse speed:%s meta:%s' % (time.time() - response.meta.get('cur_time'), response.meta))

        proxy.vali_count += 1
        proxy.speed = time.time() - response.meta.get('cur_time')
        if self.success_mark in response.text or self.success_mark is '':
            if table == self.name:
                if proxy.speed > self.timeout:
                    self.sql.del_proxy_with_id(table, proxy.id)
                else:
                    self.sql.update_proxy(table, proxy)
            else:
                if proxy.speed < self.timeout:
                    self.sql.insert_proxy(table_name = self.name, proxy = proxy)
        else:
            if table == self.name:
                self.sql.del_proxy_with_id(table_name = table, id = proxy.id)

        self.sql.commit()

    def error_parse(self, failure):
        request = failure.request
        self.log('error_parse value:%s url:%s meta:%s' % (failure.value, request.url, request.meta))

        proxy = failure.request.meta.get('proxy_info')
        table = failure.request.meta.get('table')

        if table == self.name:
            self.sql.del_proxy_with_id(table_name = table, id = proxy.id)
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

    def save_page(self, ip, data):
        filename = '{time} {ip}'.format(time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f'), ip = ip)

        if self.is_record_web_page:
            with open('%s/%s.html' % (self.dir_log, filename), 'wb') as f:
                f.write(data)
                f.close()

    def close(spider, reason):
        spider.sql.commit()
