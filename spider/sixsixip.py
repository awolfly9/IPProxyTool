# coding=utf-8


import re
import requests
import sys
import chardet
from proxy import Proxy
from spider import Spider
from utils import log


class SixSixIpSpider(Spider):
    def __init__(self, queue):
        super(SixSixIpSpider, self).__init__(queue)
        self.name = 'sixsixip'
        'http://www.66ip.cn/4.html'
        self.urls = ['http://m.66ip.cn/%s.html' % n for n in range(1, 2)]

        self.dir_log = 'log/spider/sixsixip'
        self.init()

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

                self.add_proxy(proxy = proxy)
