#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   school.py.py    
@Contact :   nickdlk@163.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/2/1/001 18:16   gxrao      1.0         None
'''

# import lib
#-*- coding: utf-8 -*-

from .validator import Validator
from scrapy import Request

import json
import time
import requests
import config
class SchoolSpider(Validator):
    name = 'school'

    def __init__(self, name = None, **kwargs):
        super(SchoolSpider, self).__init__(name, **kwargs)

        self.urls = [
            'http://210.38.250.43/index.jsp'
        ]

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 '
                          'Firefox/50.0',
        }

        self.init()

    def init(self):
            super(SchoolSpider, self).init()

            r = requests.get(url=self.urls[0], timeout=20)
            data = json.loads(r.text)
            self.origin_ip = data.get('origin', '')
            self.log('origin ip:%s' % self.origin_ip)

    def start_requests(self):
        count = self.sql.get_proxy_count(self.name)
        count_free = self.sql.get_proxy_count(config.free_ipproxy_table)

        ids = self.sql.get_proxy_ids(self.name)
        ids_free = self.sql.get_proxy_ids(config.free_ipproxy_table)

        for i in range(0, count + count_free):
            table = self.name if (i < count) else config.free_ipproxy_table
            id = ids[i] if i < count else ids_free[i - len(ids)]

            proxy = self.sql.get_proxy_with_id(table, id)
            if proxy == None:
                continue

            for url in self.urls:
                https = 'yes' if 'https' in url else 'no'

                yield Request(
                    url=url,
                    headers=self.headers,
                    dont_filter=True,
                    priority=0 if https == 'yes' else 10,
                    meta={
                        'cur_time': time.time(),
                        'download_timeout': self.timeout,
                        'proxy_info': proxy,
                        'table': table,
                        'https': https,
                        'proxy': 'http://%s:%s' % (proxy.ip, proxy.port),
                        'vali_count': proxy.vali_count,
                    },
                    callback=self.success_parse,
                    errback=self.error_parse,
                )

    def success_parse(self, response):
        proxy = response.meta.get('proxy_info')
        table = response.meta.get('table')
        proxy.https = response.meta.get('https')

        self.save_page(proxy.ip, response.body)

        if self.success_content_parse(response):
            proxy.speed = time.time() - response.meta.get('cur_time')
            proxy.vali_count += 1
            self.log('proxy_info:%s' % (str(proxy)))
            if proxy.https == 'no':
                data = json.loads(response.body)
                origin = data.get('origin')
                headers = data.get('headers')
                x_forwarded_for = headers.get('X-Forwarded-For', None)
                x_real_ip = headers.get('X-Real-Ip', None)
                via = headers.get('Via', None)

                if self.origin_ip in origin:
                    proxy.anonymity = 3
                elif via is not None:
                    proxy.anonymity = 2
                elif x_forwarded_for is not None and x_real_ip is not None:
                    proxy.anonymity = 1

                if table == self.name:
                    if proxy.speed > self.timeout:
                        self.sql.del_proxy_with_id(table_name=table, id=proxy.id)
                    else:
                        self.sql.update_proxy(table_name=table, proxy=proxy)
                else:
                    if proxy.speed < self.timeout:
                        self.sql.insert_proxy(table_name=self.name, proxy=proxy)
            else:
                self.sql.update_proxy(table_name=table, proxy=proxy)

        self.sql.commit()

    def error_parse(self, failure):
        request = failure.request
        self.log('error_parse value:%s url:%s meta:%s' % (failure.value, request.url, request.meta))
        https = request.meta.get('https')
        if https == 'no':
            table = request.meta.get('table')
            proxy = request.meta.get('proxy_info')

            if table == self.name:
                self.sql.del_proxy_with_id(table_name=table, id=proxy.id)
            else:
                # TODO... 如果 ip 验证失败应该针对特定的错误类型，进行处理
                pass