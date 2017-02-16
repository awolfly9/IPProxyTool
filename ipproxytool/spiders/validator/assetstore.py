#-*- coding: utf-8 -*-

import json
import time
import config
import utils

from scrapy.http import Request
from validator import Validator


class AssetStoreSpider(Validator):
    name = 'assetstore'

    def __init__(self, *a, **kwargs):
        super(AssetStoreSpider, self).__init__(*a, **kwargs)

        self.timeout = 10

        self.init()

    def start_requests(self):
        url = 'https://www.assetstore.unity3d.com/login'
        yield Request(
                url = url,
                headers = {
                    'Accept': 'application/json',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Host': 'www.assetstore.unity3d.com',
                    'Referer': 'https://www.assetstore.unity3d.com/en/',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 '
                                  'Firefox/50.0',
                    'X-Kharma-Version': '0',
                    'X-Requested-With': 'UnityAssetStore',
                    'X-Unity-Session': '26c4202eb475d02864b40827dfff11a14657aa41',
                },
                meta = {
                },
                dont_filter = True,
                callback = self.get_unity_version,
                errback = self.error_parse,
        )

    def get_unity_version(self, response):
        content = json.loads(response.body)
        utils.log('unity content:%s' % response.body)

        unity_version = content.get('kharma_version', '')

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Host': 'www.assetstore.unity3d.com',
            'Referer': 'https://www.assetstore.unity3d.com/en/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
            'X-Kharma-Version': unity_version,
            'X-Requested-With': 'UnityAssetStore',
            'X-Unity-Session': '26c4202eb475d02864b40827dfff11a14657aa41',
        }

        count = utils.get_table_length(self.sql, self.name)
        count_free = utils.get_table_length(self.sql, config.httpbin_table)

        for i in range(0, count + count_free):
            table = self.name if (i < count) else config.httpbin_table

            proxy = utils.get_proxy_info(self.sql, table, i)
            if proxy == None:
                continue

            url = 'https://www.assetstore.unity3d.com/api/en-US/content/overview/' + '368' + '.json'
            cur_time = time.time()
            yield Request(
                    url = url,
                    headers = headers,
                    meta = {
                        'cur_time': cur_time,
                        'download_timeout': self.timeout,
                        'proxy_info': proxy,
                        'table': table,
                        'id': proxy.get('id'),
                        'proxy': 'http://%s:%s' % (proxy.get('ip'), proxy.get('port')),
                    },
                    dont_filter = True,
                    callback = self.success_parse,
                    errback = self.error_parse,
            )
