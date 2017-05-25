# -*- coding: utf-8 -*-

import json
import logging
import web
import sys
import config

from proxy import Proxy
from sql import SqlManager

urls = (
    '/', 'index',
    '/insert', 'insert',
    '/select', 'select',
    '/delete', 'delete'
)


def run_data_server():
    sys.argv.append('0.0.0.0:%s' % config.data_port)
    app = web.application(urls, globals())
    app.run()


class index(object):
    def GET(self):
        return 'Hello World!'


class insert(object):
    def GET(self):
        try:
            sql = SqlManager()
            inputs = web.input()
            name = inputs.get('name')

            proxy = Proxy()
            proxy.set_value(
                ip=inputs.get('ip'),
                port=inputs.get('port'),
                country=inputs.get('country', None),
                anonymity=inputs.get('anonymity', None),
                https=inputs.get('https', 'no'),
                speed=inputs.get('speed', -1),
                source=inputs.get('source', name),
            )

            sql.insert_proxy(name, proxy)
        except Exception, e:
            logging.exception('insert exception msg:%s' % e)

        return False


class select(object):
    def GET(self):
        try:
            sql = SqlManager()
            inputs = web.input()
            name = inputs.get('name')
            anonymity = inputs.get('anonymity', '')
            https = inputs.get('https', '')
            order = inputs.get('order', 'speed')
            sort = inputs.get('sort', 'asc')
            count = inputs.get('count', 100)

            kwargs = {
                'anonymity': anonymity,
                'https': https,
                'order': order,
                'sort': sort,
                'count': count
            }
            result = sql.select_proxy(name, **kwargs)
            data = [{
                'ip': item.get('ip'), 'port': item.get('port'),
                'anonymity': item.get('anonymity'), 'https': item.get('https'),
                'speed': item.get('speed'), 'save_time': item.get('save_time', '')
            } for item in result]

            data = json.dumps(data, indent=4)
            return data
        except Exception, e:
            logging.exception('select exception msg:%s' % e)

        return []


class delete(object):
    def GET(self):
        try:
            sql = SqlManager()
            inputs = web.input()
            name = inputs.get('name')
            ip = inputs.get('ip')
            return sql.del_proxy_with_ip(name, ip)
        except Exception, e:
            logging.exception('delete exception msg:%s' % e)
        return False
