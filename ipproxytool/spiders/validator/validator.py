#-*- coding: utf-8 -*-

from scrapy.spiders import Spider
from sqlhelper import SqlHelper
from utils import *


class Validator(Spider):
    name = 'base'

    def __init__(self, name = None, **kwargs):
        super(Validator, self).__init__(name, **kwargs)
        self.sql = SqlHelper()
        self.dir_log = 'log/validator/%s' % self.name
        self.timeout = 10

    def init(self):
        make_dir(self.dir_log)

        command = get_create_table_command(self.name)
        self.sql.create_table(command)

    def success_parse(self, response):
        pass

    def error_parse(self, failure):
        self.log('error_parse')
        self.log('error_parse value:%s' % failure.value)

        proxy = failure.request.meta.get('proxy_info')
        table = failure.request.meta.get('table')
        id = failure.request.meta.get('id')

        if table == self.name:
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

    def save_page(self, filename, data):
        with open('%s/%s.html' % (self.dir_log, filename), 'w') as f:
            f.write(data)
            f.close()
