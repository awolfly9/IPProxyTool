# coding=utf-8

from proxy import Proxy
from .basespider import BaseSpider
from scrapy.selector import Selector
import re
from base64 import b64decode

class ProxyDBSpider(BaseSpider):
    name = 'proxydb'

    def __init__(self, *a, **kwargs):
        super(ProxyDBSpider, self).__init__(*a, **kwargs)
        self.urls = ['http://proxydb.net/?protocol=http&protocol=https&offset=%s' % n for n in range(1, 500, 50)]
        self.headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }

        self.is_record_web_page = False
        self.init()

    def parse_page(self, response):
        super(ProxyDBSpider, self).parse_page(response)
        for table_item in response.xpath('//tbody/tr'):
            ip,port = self.parse_ip(table_item.xpath('.//td[1]/script/text()').extract_first())
            country = table_item.xpath('.//td/img/@title').extract_first().strip()
            anonymity = table_item.xpath('.//td/span/text()').extract_first().strip()
            proxy = Proxy()
            proxy.set_value(
                    ip = ip,
                    port = port,
                    country = country,
                    anonymity = anonymity,
                    source = self.name
            )
            self.add_proxy(proxy = proxy)

    def parse_ip(self, page):
        ip_part1 = re.search(r'\'(.*)\'\.split',page).group(1)[::-1]
        ip_part2= ''.join([chr(int(x,16)) for x in re.findall(r'\\x([0-9A-Fa-f]{2})', page)])
        ip_part2= b64decode(ip_part2).decode('utf-8')
        port = re.search(r'pp = -(\d+) \+ (\d+);',page).groups()
        port = -int(port[0]) + int(port[1])
        return [''.join([ip_part1,ip_part2]),port]

