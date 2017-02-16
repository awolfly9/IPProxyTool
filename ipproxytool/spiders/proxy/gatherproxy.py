# coding=utf-8

import json
import random
import re
import requests

from proxy import Proxy
from basespider import BaseSpider


class GatherproxySpider(BaseSpider):
    name = 'gatherproxy'

    def __init__(self, *a, **kwargs):
        super(GatherproxySpider, self).__init__(*a, **kwargs)
        self.urls = [
            'http://gatherproxy.com/',
            'http://gatherproxy.com/proxylist/anonymity/?t=Anonymous',
            'http://gatherproxy.com/proxylist/country/?c=China',
        ]

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'gatherproxy.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 '
                          'Firefox/50.0',
        }

        self.proxies = self.get_proxy()
        self.init()

    def parse_page(self, response):
        pattern = re.compile('gp.insertPrx\((.*?)\)', re.S)
        items = re.findall(pattern, response.body)
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
                    source = self.name,
            )

            self.add_proxy(proxy = proxy)

    def get_proxy(self):
        try:
            url = 'http://127.0.0.1:8000/?name={0}'.format(self.name)
            r = requests.get(url = url)
            if r.text != None and r.text != '':
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
