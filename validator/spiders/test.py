#-*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.http import Request


class Test(Spider):
    name = 'test'

    def start_requests(self):
        url = 'http://www.baidu.com'
        yield Request(
                url = url,
                callback = self.parse
        )

    def parse(self, response):
        self.log('url:%s' % response.url)
