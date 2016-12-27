# coding=utf-8

import json
import logging
import re
import requests
from bs4 import BeautifulSoup as bs4
from lxml import html

from Proxy import Proxy
from Spider import Spider

class GatherproxySpider(Spider):
    def __init__(self, queue):
        super(GatherproxySpider, self).__init__(queue)
        self.name = 'GatherproxySpider'
        self.urls = [
            'http://gatherproxy.com/',
            'http://gatherproxy.com/proxylist/anonymity/?t=Anonymous',
        ]

    def parse_page(self, r):
        pattern = re.compile('gp.insertPrx\((.*?)\)', re.S)
        items = re.findall(pattern, r.text)
        for item in items:
            data = json.loads(item)
            #端口用的是十六进制
            port = data.get('PROXY_PORT')
            port = str(int(port, 16))

            proxy = Proxy()
            proxy.set_value(
                    ip = data.get('PROXY_IP'),
                    port = port,
                    country = data.get('PROXY_COUNTRY'),
                    anonymity = data.get('PROXY_TYPE'),
                    https = 'no',
                    speed = 1
            )

            logging.info('proxy:%s' % proxy)

            self.add_proxy(proxy = proxy)