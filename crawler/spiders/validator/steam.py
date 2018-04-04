#-*- coding: utf-8 -*-

from .validator import Validator


class SteamSpider(Validator):
    name = 'steam'

    def __init__(self, name = None, **kwargs):
        super(SteamSpider, self).__init__(name, **kwargs)

        self.timeout = 10

        self.urls = [
            'http://store.steampowered.com/app/602580/'
        ]

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'store.steampowered.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:51.0) Gecko/20100101 Firefox/51.0',
        }

        self.is_record_web_page = False

        self.init()
