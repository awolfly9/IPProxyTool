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
