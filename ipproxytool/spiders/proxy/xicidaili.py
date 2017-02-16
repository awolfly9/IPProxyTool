#-*- coding: utf-8 -*-

from proxy import Proxy
from basespider import BaseSpider
from scrapy.selector import Selector


class XiCiDaiLiSpider(BaseSpider):
    name = 'xici'

    def __init__(self, *a, **kw):
        super(XiCiDaiLiSpider, self).__init__(*a, **kw)

        self.urls = ['http://www.xicidaili.com/nn/%s' % n for n in range(1, 2)]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.xicidaili.com',
            'If-None-Match': 'W/"cb655e834a031d9237e3c33f3499bd34"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.init()

    def parse_page(self, response):
        sel = Selector(text = response.body)
        infos = sel.xpath('//tr[@class="odd"]').extract()
        for info in infos:
            val = Selector(text = info)
            ip = val.xpath('//td[2]/text()').extract_first()
            port = val.xpath('//td[3]/text()').extract_first()
            country = val.xpath('//td[4]/a/text()').extract_first()
            anonymity = val.xpath('//td[5]/text()').extract_first()

            proxy = Proxy()
            proxy.set_value(
                    ip = ip,
                    port = port,
                    country = country,
                    anonymity = anonymity,
                    source = self.name,
            )

            self.add_proxy(proxy = proxy)
