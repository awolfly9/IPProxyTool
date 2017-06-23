#-*- coding: utf-8 -*-

from .validator import Validator


class BossSpider(Validator):
    name = 'boss'
    concurrent_requests = 8

    def __init__(self, name = None, **kwargs):
        super(BossSpider, self).__init__(name, **kwargs)

        self.urls = [
            'https://www.zhipin.com/c101010100/h_101010100/?query=java&page=1&ka=page-1'
        ]

        self.headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'en-US,en;q=0.5',
            # 'Cache-Control': 'max-age=0',
            # 'Connection': 'keep-alive',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 '
                          'Firefox/50.0',
        }

        self.success_mark = '<!DOCTYPE html>'
        self.is_record_web_page = False
        self.init()
