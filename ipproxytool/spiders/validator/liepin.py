#-*- coding: utf-8 -*-

from .validator import Validator


class LiepinSpider(Validator):
    name = 'liepin'
    concurrent_requests = 8

    def __init__(self, name = None, **kwargs):
        super(LiepinSpider, self).__init__(name, **kwargs)

        self.urls = [
            'https://www.liepin.com/zhaopin/?pubTime=&ckid=17c370b0a0111aa5&fromSearchBtn=2&compkind' \
            '=&isAnalysis=&init=-1&searchType=1&dqs=%s&industryType=&jobKind=&sortFlag=15&industries=&salary'
            '=&compscale=&clean_condition=&key=%s&headckid=49963e122c30b827&curPage=%s' % ('010', 'ios', '1')
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

        self.success_mark = 'sojob-list'
        self.is_record_web_page = False
        self.init()
