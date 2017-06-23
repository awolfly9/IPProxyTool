# coding=utf-8

from proxy import Proxy
from .basespider import BaseSpider
from scrapy.selector import Selector


class ProxyDBSpider(BaseSpider):
    name = 'proxydb'

    def __init__(self, *a, **kwargs):
        super(ProxyDBSpider, self).__init__(*a, **kwargs)

        self.urls = ['http://proxydb.net/?protocol=http&protocol=https&offset=%s' % n for n in range(1, 500, 50)]
        self.headers = {
            'Host': 'proxydb.net',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.is_record_web_page = False
        self.init()

    def parse_page(self, response):
        super(ProxyDBSpider, self).parse_page(response)

        data = response.xpath('//tbody/tr').extract()
        for i, d in enumerate(data):
            sel = Selector(text = d)

            ip_port = sel.xpath('//td/a/text()').extract_first()
            ip = ip_port.split(':')[0]
            port = ip_port.split(':')[1]
            country = sel.xpath('//td/img/@title').extract_first()
            anonymity = sel.xpath('//td/span[@class="text-success"]/text()').extract_first()

            proxy = Proxy()
            proxy.set_value(
                    ip = ip,
                    port = port,
                    country = country,
                    anonymity = anonymity,
                    source = self.name
            )

            self.add_proxy(proxy = proxy)
