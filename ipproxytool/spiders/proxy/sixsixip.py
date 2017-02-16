# coding=utf-8

import re

from proxy import Proxy
from basespider import BaseSpider


class SixSixIpSpider(BaseSpider):
    name = 'sixsixip'

    def __init__(self, *a, **kwargs):
        super(SixSixIpSpider, self).__init__(*a, **kwargs)

        self.urls = ['http://m.66ip.cn/%s.html' % n for n in range(1, 2)]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'm.66ip.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.init()

    def parse_page(self, response):
        pattern = re.compile('<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>',
                             re.S)
        items = re.findall(pattern, response.body)
        for i, item in enumerate(items):
            if i >= 1:
                proxy = Proxy()
                proxy.set_value(
                        ip = item[0],
                        port = item[1],
                        country = item[2],
                        anonymity = item[3],
                        source = self.name
                )

                self.add_proxy(proxy = proxy)
