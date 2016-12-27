# coding=utf-8

import logging
import urllib
import re
import requests

from Proxy import Proxy
from Spider import Spider
from bs4 import BeautifulSoup


class FreeProxyListsSpider(Spider):
    def __init__(self, queue):
        super(FreeProxyListsSpider, self).__init__(queue)
        self.name = 'FreeProxyLists'
        self.urls = [
            'http://www.freeproxylists.net/'
        ]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Host': 'www.freeproxylists.net',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

    def parse_page(self, r):
        pattern = re.compile('<tr class=(.*?)</tr>', re.S)
        items = re.findall(pattern = pattern, string = r.text)
        for i, item in enumerate(items):
            if i > 0:
                if 'async' in item:
                    continue

                ip_pattern = re.compile('IPDecode\(\"(.*?)\"\)', re.S)
                ip_decode = re.findall(ip_pattern, item)[0]
                ip_url = urllib.unquote(ip_decode)
                ip_soup = BeautifulSoup(ip_url, 'lxml')
                ip = ip_soup.text.encode()

                item = '<tr class=' + item + '</tr>'
                soup = BeautifulSoup(item, 'lxml')
                tbodys = soup.find_all('td')

                proxy = Proxy()
                proxy.set_value(
                        ip = ip,
                        port = tbodys[1].text.encode(),
                        country = tbodys[4].text.encode(),
                        anonymity = tbodys[3].text.encode(),
                        https = 'no',
                        speed = 1
                )

                self.add_proxy(proxy = proxy)