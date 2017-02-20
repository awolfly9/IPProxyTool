#-*- coding: utf-8 -*-


class Proxy(object):
    def __init__(self):
        self.index = 10000
        self.ip = ''
        self.port = ''
        self.country = ''
        self.anonymity = ''
        self.https = ''
        self.speed = ''
        self.source = ''

    def __str__(self):
        data = {
            'ip': self.ip,
            'port': self.port,
            'country': self.country,
            'anonymity': self.anonymity,
            'https': self.https,
            'speed': self.speed,
            'source': self.source
        }

        return str(data)

    def set_value(self, ip, port, country, anonymity, source = 'unkonw', https = 'no', speed = -1):
        self.ip = ip
        self.port = port
        self.country = country
        self.anonymity = self.get_anonymity_type(anonymity)
        self.https = https
        self.speed = speed
        self.source = source

    def get_anonymity_type(self, anonymity):
        '''There are 3 levels of proxies according to their anonymity.

            Level 1 - Elite Proxy / Highly Anonymous Proxy: The web server can't detect whether you are using a proxy.
            Level 2 - Anonymous Proxy: The web server can know you are using a proxy, but it can't know your real IP.
            Level 3 - Transparent Proxy: The web server can know you are using a proxy and it can also know your real
            IP.
        '''

        if anonymity == u'高匿代理' or anonymity == u'高匿名' or anonymity == 'elite proxy' or \
                        anonymity == u'超级匿名' or anonymity == u'High':
            return '1'
        elif anonymity == u'匿名' or anonymity == 'anonymous' or anonymity == u'普通匿名' or anonymity == u'Medium':
            return '2'
        elif anonymity == u'透明' or anonymity == 'transparent' or anonymity == u'No':
            return '3'
        else:
            return '3'
