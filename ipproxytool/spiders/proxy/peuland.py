#-*- coding: utf-8 -*-

import json
import logging
import requests
import base64
import utils

from scrapy.http import Request
from proxy import Proxy
from utils import log
from basespider import BaseSpider


class PeulandSpider(BaseSpider):
    name = 'peuland'

    def __init__(self, *a, **kwargs):
        super(PeulandSpider, self).__init__(*a, **kwargs)
        self.urls = ['https://proxy.peuland.com/proxy_list_by_category.htm']
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'proxy.peuland.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.meta = {
            'download_timeout': self.timeout,
            'cookiejar': 1,
        }

        self.timeout = 20

        self.init()

    def start_requests(self):
        for i, url in enumerate(self.urls):
            yield Request(
                    url = url,
                    headers = self.headers,
                    meta = self.meta,
                    dont_filter = True,
                    callback = self.parse_page,
                    errback = self.error_parse,
            )

    def parse_page(self, response):

        utils.log('cookiejar:%s' % response.meta.get('cookiejar'))

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'proxy.peuland.com',
            'Referer': 'https://proxy.peuland.com/proxy_list_by_category.htm',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
            'X-Requested-With': 'XMLHttpRequest',
        }

        cookies = {
            'peuland_id': '649e2152bad01e29298950671635e44a',
            'CNZZDATA1253154494': '179614273-1483168549-%7C1483168549',
            'peuland_md5': '9b941affd9b676f62ab93081f6cc9a1b',
            'w_h': '800',
            'w_w': '1280',
            'w_cd': '24',
            'w_a_h': '709',
            'w_a_w': '1280',
            'PHPSESSID': '5g8o2ubj6t4fenh2dklnrcr6n4',
            'php_id': '1288641658',
        }

        for i in range(1, 3):
            fromdata = {
                'country_code': '',
                'is_clusters': '',
                'is_https': '',
                'level_type': '',
                'search_type': 'all',
                'type': '',
                'page': i,
            }

            url = 'https://proxy.peuland.com/proxy/search_proxy.php'

            req = None
            ret = False
            for j in range(3):
                try:
                    req = requests.post(url = url, headers = headers, data = fromdata, cookies = cookies, timeout = 50)
                    log('PeulandSpider parse_page req.text:%s' % req.url)
                    ret = True
                    break
                except Exception, e:
                    log('PeulandSpider parse_page exception:%s' % str(e), logging.WARNING)
                    continue

            if ret == False:
                continue

            result = json.loads(req.text)
            items = result.get('data')
            for item in items:
                ip = base64.b64decode(item.get('ip'))
                port = base64.b64decode(item.get('port'))
                type = base64.b64decode(item.get('type'))
                https = base64.b64decode(item.get('is_https'))
                level_type = base64.b64decode(item.get('level_type'))
                time_total = base64.b64decode(item.get('time_total'))
                time_downloadspeed = base64.b64decode(item.get('time_downloadspeed'))
                country = base64.b64decode(item.get('country'))
                country_zw = base64.b64decode(item.get('country_zw'))
                status_cnc = base64.b64decode(item.get('status_cnc'))
                status_ctn = base64.b64decode(item.get('status_ctn'))

                proxy = Proxy()
                proxy.set_value(
                        ip = ip,
                        port = port,
                        country = country_zw,
                        anonymity = level_type,
                        source = self.name,
                )

                self.add_proxy(proxy)
