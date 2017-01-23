# coding=utf-8

import json
import logging
import random
import re
import requests
from bs4 import BeautifulSoup as bs4
from lxml import html

from proxy import Proxy
from spider import Spider


class GatherproxySpider(Spider):
    def __init__(self, queue):
        super(GatherproxySpider, self).__init__(queue)
        self.name = 'gather'
        self.urls = [
            'http://gatherproxy.com/',
            'http://gatherproxy.com/proxylist/anonymity/?t=Anonymous',
        ]

        self.dir_log = 'log/spider/gather'
        self.proxies = self.get_proxy()
        self.init()

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

            self.add_proxy(proxy = proxy)

    def get_proxy(self):
        url = 'http://127.0.0.1:8000/?name={0}'.format(self.name)
        r = requests.get(url = url)
        if r.text != None and r.text != '':
            try:
                data = json.loads(r.text)
                if len(data) > 0:
                    proxy = random.choice(data)
                    ip = proxy.get('ip')
                    port = proxy.get('port')
                    address = '%s:%s' % (ip, port)

                    proxies = {
                        'http': 'http://%s' % address
                    }
                    return proxies
            except:
                return None

        return None
