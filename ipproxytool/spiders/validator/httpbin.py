#-*- coding: utf-8 -*-

from validator import Validator


class HttpBinSpider(Validator):
    name = 'httpbin'

    def __init__(self, name = None, **kwargs):
        super(HttpBinSpider, self).__init__(name, **kwargs)

        self.timeout = 5
        self.urls = [
            'http://httpbin.org/get'
        ]

        self.init()
