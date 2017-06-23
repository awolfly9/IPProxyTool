#-*- coding: utf-8 -*-

import time
import config
import utils

from .validator import Validator
from scrapy.http import FormRequest


class LagouSpider(Validator):
    name = 'lagou'
    concurrent_requests = 8

    def __init__(self, name = None, **kwargs):
        super(LagouSpider, self).__init__(name, **kwargs)

        self.urls = [
            'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'
        ]

        self.headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'en-US,en;q=0.5',
            # 'Cache-Control': 'max-age=0',
            # 'Connection': 'keep-alive',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 '
                          'Firefox/50.0',
        }

        self.is_record_web_page = True
        self.success_mark = 'success'
        self.init()

    def start_requests(self):
        count = self.sql.get_proxy_count(self.name)
        count_httpbin = self.sql.get_proxy_count(config.httpbin_table)

        ids = self.sql.get_proxy_ids(self.name)
        ids_httpbin = self.sql.get_proxy_ids(config.httpbin_table)

        for i in range(0, count + count_httpbin):
            table = self.name if (i < count) else config.httpbin_table
            id = ids[i] if i < count else ids_httpbin[i - len(ids)]

            proxy = self.sql.get_proxy_with_id(table, id)
            if proxy == None:
                continue

            for url in self.urls:
                cur_time = time.time()
                yield FormRequest(
                        url = url,
                        headers = self.headers,
                        method = 'POST',
                        meta = {
                            'cur_time': cur_time,
                            'download_timeout': self.timeout,
                            'proxy_info': proxy,
                            'table': table,
                            'id': proxy.get('id'),
                            'proxy': 'http://%s:%s' % (proxy.get('ip'), proxy.get('port')),
                            'vali_count': proxy.get('vali_count', 0),
                        },
                        cookies = {
                            'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1488937030',
                            '_ga': 'GA1.2.40497390.1488937014',
                            'TG-TRACK-CODE': 'search_code',
                            'index_location_city': '%E5%8C%97%E4%BA%AC',
                            'LGRID': '20170308093710-bf6755eb-039f-11e7-8025-525400f775ce',
                            'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1488881288,1488936799,1488936947,1488937014',
                            'JSESSIONID': 'BDCBB6167F960CE43AF54B75A651F586',
                            'LGSID': '20170308093653-b59316f0-039f-11e7-9229-5254005c3644',
                            'LGUID': '20170308093653-b593185f-039f-11e7-9229-5254005c3644',
                            'user_trace_token': '20170308093654-723efcfac8fb4c28a670d073d5113e02',
                            'SEARCH_ID': '4db4dc3dea1c46b49018ae5421b53ffa'
                        },
                        formdata = {
                            'first': 'true',
                            'kd': 'ios',
                            'pn': '1',
                        },
                        dont_filter = True,
                        callback = self.success_parse,
                        errback = self.error_parse,
                )
