#-*- coding: utf-8 -*-

from .validator import Validator


class AmazonCnSpider(Validator):
    name = 'amazoncn'

    def __init__(self, name = None, **kwargs):
        super(AmazonCnSpider, self).__init__(name, **kwargs)

        self.timeout = 5

        self.urls = [
            'https://www.amazon.cn/dp/B00ID363S4',
            'https://www.amazon.cn/gp/product/B01BDBJ71W',
            'https://www.amazon.cn/gp/product/B06XBHPZNC',
        ]

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'www.amazon.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 '
                          'Firefox/50.0',
        }

        self.init()

    def success_content_parse(self, response):
        if 'Amazon CAPTCHA' in response.text:
            return False
        return True
        
        
        
        
