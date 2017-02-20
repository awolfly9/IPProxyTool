#-*- coding: utf-8 -*-

import utils

from scrapy import Selector
from basespider import BaseSpider
from proxy import Proxy


class IpOneEightOneSpider(BaseSpider):
    name = 'ip181'

    def __init__(self, *a, **kw):
        super(IpOneEightOneSpider, self).__init__(*a, **kw)

        self.urls = ['http://www.ip181.com/']
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'www.ip181.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.init()

    def parse_page(self, response):
        self.write(response.body)

        sel = Selector(response)
        infos = sel.xpath('//tbody/tr').extract()
        for i, info in enumerate(infos):
            if i == 0:
                continue

            val = Selector(text = info)
            ip = val.xpath('//td[1]/text()').extract_first()
            port = val.xpath('//td[2]/text()').extract_first()
            country = val.xpath('//td[6]/text()').extract_first()
            anonymity = val.xpath('//td[3]/text()').extract_first()
            https = val.xpath('//td[4]/text()').extract_first()

            proxy = Proxy()
            proxy.set_value(
                    ip = ip,
                    port = port,
                    country = country,
                    anonymity = anonymity,
                    source = self.name,
            )

            self.add_proxy(proxy = proxy)
