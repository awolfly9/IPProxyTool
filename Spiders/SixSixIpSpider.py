# coding=utf-8
import logging
import re
import requests
import sys
import chardet
from Proxy import Proxy
from Spider import Spider


class SixSixIpSpider(Spider):
    def __init__(self, queue):
        super(SixSixIpSpider, self).__init__(queue)
        self.name = 'SixSixIpSpider'
        self.urls = ['http://m.66ip.cn/%s.html' % n for n in ['index'] + range(1, 10)]

    def parse_page(self, r):
        pattern = re.compile('<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>',
                             re.S)
        items = re.findall(pattern, r.content)
        for i, item in enumerate(items):
            if i >= 1:
                proxy = Proxy()
                proxy.set_value(
                        ip = item[0],
                        port = item[1],
                        country = item[2],
                        anonymity = item[3],
                        https = 'no',
                        speed = 1
                )

                logging.info('proxy:%s' % proxy)

                self.add_proxy(proxy = proxy)
