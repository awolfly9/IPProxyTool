#-*- coding: utf-8 -*-

from validator import Validator


class DoubanSpider(Validator):
    name = 'douban'

    def __init__(self, name = None, **kwargs):
        super(DoubanSpider, self).__init__(name, **kwargs)

        self.timeout = 5

        self.urls = [
            'https://movie.douban.com/subject/3434070/?from=subject-page'
        ]

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'movie.douban.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 '
                          'Firefox/50.0',
        }

        self.init()
