# -*- coding: utf-8 -*-

from .validator import Validator


class BBSSpider(Validator):
    name = 'bbs'
    concurrent_requests = 8

    def __init__(self, name = None, **kwargs):
        super(BBSSpider, self).__init__(name, **kwargs)

        self.urls = [
            'http://www.autohome.com.cn/beijing/',
            'http://club.autohome.com.cn/bbs/thread-c-2098-64053713-1.html',
            'http://club.autohome.com.cn/bbs/thread-c-2098-61435076-1.html',
            'http://club.autohome.com.cn/bbs/threadqa-c-4034-63834038-1.html',
            'http://club.autohome.com.cn/bbs/threadqa-c-4034-63083758-1.html',
            'http://club.autohome.com.cn/bbs/threadqa-c-4044-64310067-1.html',
            'http://club.autohome.com.cn/bbs/threadqa-c-4044-64328047-1.html',
            'http://club.autohome.com.cn/bbs/thread-c-4044-63233315-1.html',
            'http://club.autohome.com.cn/bbs/threadqa-c-4044-62349867-1.html',
            'http://club.autohome.com.cn/bbs/thread-c-4034-63846295-1.html',
        ]

        self.headers = {
            'Host': 'club.autohome.com.cn',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 '
                          'Firefox/50.0',
        }

        self.success_mark = 'conmain'
        self.is_record_web_page = False
        self.init()
