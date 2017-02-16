#-*- coding: utf-8 -*-

import re

from proxy import Proxy
from basespider import BaseSpider


class KuaiDaiLiSpider(BaseSpider):
    name = 'kuaidaili'

    def __init__(self, *a, **kwargs):
        super(KuaiDaiLiSpider, self).__init__(*a, **kwargs)

        self.urls = ['http://www.kuaidaili.com/free/inha/%s/' % i for i in range(1, 2)]

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'www.kuaidaili.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.init()

    def parse_page(self, response):
        pattern = re.compile(
                '<tr>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>('
                '.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?</tr>',
                re.S)
        items = re.findall(pattern, response.body)

        for item in items:
            proxy = Proxy()
            proxy.set_value(
                    ip = item[0],
                    port = item[1],
                    country = item[4],
                    anonymity = item[2],
                    source = self.name,
            )

            self.add_proxy(proxy)
