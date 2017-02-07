#-*- coding: utf-8 -*-

from validator import Validator


class GatherSpider(Validator):
    name = 'gather'

    def __init__(self, name = None, **kwargs):
        super(GatherSpider, self).__init__(name, **kwargs)

        self.timeout = 10
        self.urls = [
            'http://gatherproxy.com/proxylist/anonymity/?t=Anonymous',
            'http://gatherproxy.com/proxylist/country/?c=China'
        ]

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'gatherproxy.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 '
                          'Firefox/50.0',
        }

        self.init()
