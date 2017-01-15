#-*- coding: utf-8 -*-
import re

from Proxy import Proxy
from Spider import Spider

class KuaiDaiLiSpider(Spider):
    def __init__(self, queue):
        super(KuaiDaiLiSpider, self).__init__(queue)

        self.name = 'kuaidaili'
        self.urls = ['http://www.kuaidaili.com/free/inha/%s/' % i for i in range(1, 5)]

    def parse_page(self, r):
        pattern = re.compile('<tr>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?</tr>', re.S)
        items = re.findall(pattern, r.text)

        for item in items:
            proxy = Proxy()
            proxy.set_value(
                ip = item[0],
                port = item[1],
                country = item[4],
                anonymity = item[2],
                https = 'no',
                speed = '-1',
            )

            print('proxy:%s' % str(proxy))
            self.add_proxy(proxy)





