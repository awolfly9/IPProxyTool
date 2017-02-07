#-*- coding: utf-8 -*-

import json
import web
import sys
import config

from sqlhelper import SqlHelper

urls = (
    '/', 'index',
    '/select', 'select',
    '/delete', 'delete'
)

sql = SqlHelper()


def start_api_server():
    sys.argv.append('0.0.0.0:%s' % config.data_port)
    app = web.application(urls, globals())
    app.run()


class index(object):
    def GET(self):
        return "Hello, world!"


class select(object):
    def GET(self):
        inputs = web.input()
        print(inputs)
        name = inputs.get('name')
        command = "SELECT * FROM {0}".format(name)
        result = sql.query(command)
        data = [{'ip': item[1], 'port': item[2], 'speed': item[6]} for item in result]
        data = json.dumps(data, indent = 4)
        return data


class delete(object):
    def GET(self):
        inputs = web.input()
        name = inputs.get('name')
        ip = inputs.get('ip')
        command = "DELETE FROM {0} WHERE ip=\'{1}\'".format(name, ip)
        return sql.execute(command)
