#-*- coding: utf-8 -*-

import json
import time
import datetime
import logging
import requests
import config
import utils

from scrapy import Request
from validator import Validator


class HttpBinSpider(Validator):
    name = 'httpbin'
    concurrent_requests = 4

    def __init__(self, name = None, **kwargs):
        super(HttpBinSpider, self).__init__(name, **kwargs)
        self.timeout = 20
        self.urls = [
            'http://httpbin.org/get?show_env=1',
            'https://httpbin.org/get?show_env=1',
        ]
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Host": "httpbin.org",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:51.0) Gecko/20100101 Firefox/51.0"
        }

        self.origin_ip = ''

        self.init()

    def start_requests(self):
        r = requests.get(url = self.urls[0])
        data = json.loads(r.text)
        self.origin_ip = data.get('origin', '')
        utils.log('origin ip:%s' % self.origin_ip)

        count = utils.get_table_length(self.sql, self.name)
        count_free = utils.get_table_length(self.sql, config.free_ipproxy_table)

        ids = utils.get_table_ids(self.sql, self.name)
        ids_free = utils.get_table_ids(self.sql, config.free_ipproxy_table)

        for i in range(0, count + count_free):
            table = self.name if (i < count) else config.free_ipproxy_table
            id = ids[i] if i < count else ids_free[i - len(ids)]

            proxy = utils.get_proxy_info(self.sql, table, id)
            if proxy == None:
                continue

            for url in self.urls:
                https = 'yes' if 'https' in url else 'no'

                yield Request(
                        url = url,
                        headers = self.headers,
                        dont_filter = True,
                        priority = 0 if https == 'yes' else 10,
                        meta = {
                            'cur_time': time.time(),
                            'download_timeout': self.timeout,
                            'proxy_info': proxy,
                            'table': table,
                            'id': proxy.get('id'),
                            'https': https,
                            'proxy': 'http://%s:%s' % (proxy.get('ip'), proxy.get('port')),
                            'vali_count': proxy.get('vali_count'),
                        },
                        callback = self.success_parse,
                        errback = self.error_parse,
                )

    def success_parse(self, response):
        utils.log('success_parse proxy:%s meta:%s' % (str(response.meta.get('proxy_info')), response.meta))

        proxy = response.meta.get('proxy_info')
        table = response.meta.get('table')
        id = response.meta.get('id')
        ip = proxy.get('ip')
        https = response.meta.get('https')

        self.save_page(ip, response.body)

        if response.body.find(self.success_mark) or self.success_mark is '':
            speed = time.time() - response.meta.get('cur_time')
            utils.log('speed:%s table:%s id:%s https:%s' % (speed, table, id, https))

            if https == 'no':
                data = json.loads(response.body)
                origin = data.get('origin')

                headers = data.get('headers')
                x_forwarded_for = headers.get('X-Forwarded-For', None)
                x_real_ip = headers.get('X-Real-Ip', None)
                via = headers.get('Via', None)
                anonymity = 3

                if self.origin_ip in origin:
                    anonymity = 3
                elif via is not None:
                    anonymity = 2
                elif x_forwarded_for is not None and x_real_ip is not None:
                    anonymity = 1

                if table == self.name:
                    if speed > self.timeout:
                        command = utils.get_delete_data_command(table, id)
                        self.sql.execute(command)
                    else:
                        # command = utils.get_update_data_command(table, id, speed)
                        # self.sql.execute(command)
                        vali_count = response.meta.get('vali_count', 0) + 1
                        command = "UPDATE {name} SET speed={speed}, https='{https}', vali_count={vali_count}, " \
                                  "anonymity={anonymity} WHERE id={id}". \
                            format(name = self.name, speed = speed, https = https, vali_count = vali_count,
                                   anonymity = anonymity, id = id)
                        self.sql.execute(command)
                else:
                    if speed < self.timeout:
                        command = utils.get_insert_data_command(self.name)
                        msg = (None, proxy.get('ip'), proxy.get('port'), proxy.get('country'), anonymity,
                               https, speed, proxy.get('source'), None, 1)

                        self.sql.insert_data(command, msg, commit = True)
            elif https == 'yes':
                command = "UPDATE {name} SET https=\'{https}\' WHERE ip=\'{ip}\'". \
                    format(name = self.name, https = https, ip = ip)
                self.sql.execute(command)
            else:
                pass

    def error_parse(self, failure):
        request = failure.request
        utils.log('error_parse value:%s url:%s meta:%s' % (failure.value, request.url, request.meta))
        https = request.meta.get('https')
        if https == 'no':
            table = request.meta.get('table')
            id = request.meta.get('id')

            if table == self.name:
                command = utils.get_delete_data_command(table, id)
                self.sql.execute(command)
            else:
                # TODO... 如果 ip 验证失败应该针对特定的错误类型，进行处理
                pass
