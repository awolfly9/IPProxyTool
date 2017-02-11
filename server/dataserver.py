#-*- coding: utf-8 -*-

import json
import web
import sys
import config
import utils

from proxy import Proxy
from sqlhelper import SqlHelper

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
        return "Hello, world!"


class insert(object):
    def GET(self):
        try:
            sql = SqlHelper()

            inputs = web.input()
            name = inputs.get('name')

            proxy = Proxy()
            proxy.set_value(
                    ip = inputs.get('ip'),
                    port = inputs.get('port'),
                    country = inputs.get('country', None),
                    anonymity = inputs.get('anonymity', None),
                    https = inputs.get('https', 'no'),
                    speed = inputs.get('speed', -1),
                    source = inputs.get('source', name),
            )

            utils.sql_insert_proxy(sql, name, proxy)

            command = "SELECT ip FROM {0} WHERE ip={1} AND port={2}".format(name, inputs.get('ip'), inputs.get('port'))
            res = sql.query_one(command)
            return res is None
        except:
            pass

        return False


class select(object):
    def GET(self):
        try:
            sql = SqlHelper()

            inputs = web.input()
            name = inputs.get('name')
            command = "SELECT * FROM {0}".format(name)
            result = sql.query(command)
            data = [{'ip': item[1], 'port': item[2], 'speed': item[6]} for item in result]
            data = json.dumps(data, indent = 4)
            return data
        except:
            pass

        return []


class delete(object):
    def GET(self):
        try:
            sql = SqlHelper()

            inputs = web.input()
            name = inputs.get('name')
            ip = inputs.get('ip')
            command = "DELETE FROM {0} WHERE ip=\'{1}\'".format(name, ip)
            sql.execute(command)

            command = "SELECT ip FROM {0} WHERE ip=\'{1}\'".format(name, ip)
            res = sql.query_one(command)
            return res is None
        except:
            pass
        return False
