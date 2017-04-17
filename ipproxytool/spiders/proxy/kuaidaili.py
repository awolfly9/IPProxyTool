#-*- coding: utf-8 -*-

import re
import time
import utils
from pyv8 import PyV8

from scrapy import Request
from proxy import Proxy
from basespider import BaseSpider


class KuaiDaiLiSpider(BaseSpider):
    name = 'kuaidaili'

    def __init__(self, *a, **kwargs):
        super(KuaiDaiLiSpider, self).__init__(*a, **kwargs)

        self.urls = ['http://www.kuaidaili.com/free/inha/%s/' % i for i in range(1, 5)]

        self.headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language': 'en-US,en;q=0.5',
            # 'Connection': 'keep-alive',
            'Host': 'www.kuaidaili.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 Firefox/52.0',
            # 'Referer': 'http://www.kuaidaili.com/free/inha/1/',
        }

        self.is_record_web_page = False
        self.init()
        # self.meta['dont_redirect'] = True
        # self.meta['handle_httpstatus_list'] = [521, 302]

    # def start_requests(self):
    #     yield Request(
    #             url = self.urls[0],
    #             headers = self.headers,
    #             meta = self.meta,
    #             dont_filter = True,
    #             callback = self.deal_js,
    #             errback = self.error_parse,
    #     )
    #
    # def deal_js(self, response):
    #     self.log(response.body)
    #     # 提取其中的JS加密函数
    #     js_func = ''.join(re.findall(r'(function .*?)</script>', response.body))
    #     # 提取其中执行JS函数的参数
    #     js_arg = ''.join(re.findall(r'setTimeout\(\"\D+\((\d+)\)\"', response.body))
    #     # 修改JS函数，使其返回Cookie内容
    #     js_func = js_func.replace('eval("qo=eval;qo(po);")', 'return po')
    #     # 执行JS获取Cookie
    #     cookie_str = self.execute_JS(js_func, js_arg)
    #     cookies = self.parse_cookie(cookie_str)
    #     for i, url in enumerate(self.urls):
    #         return Request(
    #                 url = url,
    #                 headers = self.headers,
    #                 cookies = cookies,
    #                 meta = self.meta,
    #                 dont_filter = True,
    #                 callback = self.parse_page,
    #                 errback = self.error_parse,
    #         )
    #
    # def execute_JS(self, js_func_string, arg):
    #     ctxt = PyV8.JSContext()
    #     ctxt.enter()
    #     func = ctxt.eval("({js})".format(js = js_func_string))
    #     return func(arg)
    #
    # def parse_cookie(self, string):
    #     string = string.replace("document.cookie='", "")
    #     clearance = string.split(';')[0]
    #     return {clearance.split('=')[0]: clearance.split('=')[1]}

    def parse_page(self, response):
        pattern = re.compile(
                '<tr>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>('
                '.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?</tr>',
                re.S)
        items = re.findall(pattern, response.body)

        for item in items:
            proxy = Proxy()
            proxy.set_value(
                    ip = item[0],
                    port = item[1],
                    country = item[4],
                    anonymity = item[2],
                    source = self.name,
            )

            self.add_proxy(proxy)
