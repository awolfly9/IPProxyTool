#-*- coding: utf-8 -*-

from scrapy import Selector
from .basespider import BaseSpider
from proxy import Proxy

class data5uSpider(BaseSpider):
    name = 'data5u'

    def __init__(self, *a, **kw):
        # 在类的继承中，如果重定义某个方法，该方法会覆盖父类的同名方法
        # 但有时，我们希望能同时实现父类的功能，这时，我们就需要调用父类的方法了，可通过使用 super 来实现，比如：
        super(data5uSpider, self).__init__(*a, **kw)

        self.urls = ['http://www.data5u.com/free/']
        self.headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate, sdch',
            # 'Accept-Language': 'zh-CN,zh;q=0.8',
            # 'Connection': 'keep-alive',
            'Host': 'www.data5u.com',
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        }

        self.init()

    def parse_page(self, response):
        self.write(response.body)

        sel = Selector(response)
        infos = sel.xpath('//ul[@class="l2"]').extract()
        for i, info in enumerate(infos):
            val = Selector(text = info)
            ip = val.xpath('//ul[@class="l2"]/span[1]/li/text()').extract_first()
            port = val.xpath('//ul[@class="l2"]/span[2]/li/text()').extract_first()
            anonymity = val.xpath('//ul[@class="l2"]/span[3]/li/text()').extract_first()
            https = val.xpath('//ul[@class="l2"]/span[4]/li/text()').extract_first()
            country = val.xpath('//ul[@class="l2"]/span[5]/li/a/text()').extract_first()

            proxy = Proxy()
            proxy.set_value(
                    ip = ip,
                    port = port,
                    country = country,
                    anonymity = anonymity,
                    source = self.name,
            )

            self.add_proxy(proxy = proxy)
