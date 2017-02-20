#-*- coding: utf-8 -*-

import utils

from scrapy import Selector
from basespider import BaseSpider
from proxy import Proxy


class ProxylistplusSpider(BaseSpider):
    name = 'proxylistplus'

    def __init__(self, *a, **kw):
        super(ProxylistplusSpider, self).__init__(*a, **kw)

        self.urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-%s' % n for n in range(1, 3)]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'list.proxylistplus.com',
            'If-Modified-Since': 'Mon, 20 Feb 2017 07:47:35 GMT',
            'If-None-Match': 'list381487576865',
            'Referer': 'https://list.proxylistplus.com/Fresh-HTTP-Proxy',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:51.0) Gecko/20100101 Firefox/51.0',
        }

        self.is_record_web_page = True
        self.init()

    def parse_page(self, response):
        self.write(response.body)

        sel = Selector(response)
        infos = sel.xpath('//table[@class="bg"]/tr').extract()
        for i, info in enumerate(infos):
            if i == 0:
                continue

            val = Selector(text = info)
            ip = val.xpath('//td[2]/text()').extract_first()
            port = val.xpath('//td[3]/text()').extract_first()
            country = val.xpath('//td[5]/text()').extract_first()
            anonymity = val.xpath('//td[4]/text()').extract_first()

            proxy = Proxy()
            proxy.set_value(
                    ip = ip,
                    port = port,
                    country = country,
                    anonymity = anonymity,
                    source = self.name,
            )

            self.add_proxy(proxy = proxy)
