# coding=utf-8

import re
import requests
import logging

import time
import Queue
from bs4 import BeautifulSoup

from Proxy import Proxy
from Spider import Spider

class UsProxySpider(Spider):
    def __init__(self, queue):
        super(UsProxySpider, self).__init__(queue)
        self.name = 'UsProxySpider'
        self. urls = [
            'http://www.sslproxies.org/',
            'http://www.us-proxy.org/',
            'http://free-proxy-list.net/uk-proxy.html',
            'http://www.socks-proxy.net/',
        ]

    def parse_page(self, r):
        pattern = re.compile(
                '<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>('
                '.*?)</td><td>(.*?)</td></tr>',
                re.S)
        items = re.findall(pattern, r.text)

        #proxies = {}
        if items is not None:
            for item in items:
                #print('ip:%s port:%s' %(item[0], item[1]))
                proxy = Proxy()
                proxy.set_value(
                        ip = item[0],
                        port = item[1],
                        country = item[3],
                        anonymity = item[4],
                        https = item[6].lower(),
                        speed = 1
                )

                self.add_proxy(proxy)

if __name__ == "__main__":
    queue = []
    spider = UsProxySpider(queue)
    spider.run()
