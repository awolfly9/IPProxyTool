# coding=utf-8

import re

from proxy import Proxy
from basespider import BaseSpider


class UsProxySpider(BaseSpider):
    name = 'usproxy'

    def __init__(self, *a, **kwargs):
        super(UsProxySpider, self).__init__(*a, **kwargs)

        self.urls = [
            'http://www.sslproxies.org/',
            'http://www.us-proxy.org/',
            'http://free-proxy-list.net/uk-proxy.html',
            'http://www.socks-proxy.net/',
        ]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.us-proxy.org',
            'If-Modified-Since': 'Tue, 24 Jan 2017 03:32:01 GMT',
            'Referer': 'http://www.sslproxies.org/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.init()

    def parse_page(self, response):
        pattern = re.compile(
                '<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>('
                '.*?)</td><td>(.*?)</td></tr>',
                re.S)
        items = re.findall(pattern, response.body)

        if items is not None:
            for item in items:
                proxy = Proxy()
                proxy.set_value(
                        ip = item[0],
                        port = item[1],
                        country = item[3],
                        anonymity = item[4],
                        source = self.name,
                )

                self.add_proxy(proxy)
