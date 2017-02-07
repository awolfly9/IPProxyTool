# coding=utf-8

import logging
import json
import urllib
import urlparse

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from sqlhelper import SqlHelper
from utils import *
from config import *


class IpProxyServer(BaseHTTPRequestHandler):
    #http://127.0.0.1:8000/?name=douban
    def do_GET(self):
        sql = SqlHelper()
        dict = {}
        str_count = ''
        condition = ''

        try:
            if self.path == '/favicon.ico':
                self.send_response(200)
                self.end_headers()
                self.wfile.write('/favicon.ico')
                return

            parse_result = urlparse.urlparse(self.path)
            query = urllib.unquote(parse_result.query)

            # 分离参数
            if query.find('&') != -1:
                params = query.split('&')
                for param in params:
                    dict[param.split('=')[0]] = param.split('=')[1]
            else:
                if query != '':
                    dict[query.split('=')[0]] = query.split('=')[1]

            log('dict:%s' % str(dict))

            i = 0
            for key, value in dict.items():
                log('key:%s, value:%s' % (key, value))
                if key == 'type':
                    cond = 'anonymity="' + value + '"'
                    if i > 0:
                        condition = condition + ' And '
                    condition = condition + cond
                    i = i + 1
                elif key == 'country':
                    cond = 'country="' + value.decode('utf-8') + '"'
                    if i > 0:
                        condition = condition + ' And '

                    condition = condition + cond
                    i = i + 1
                elif key == 'count':
                    str_count = 'limit ' + value
                elif key == 'table':
                    pass
                else:
                    log('没有处理的参数:%s 值为:%s' % (key, value), logging.WARNING)

            log('condition:%s, count:%s' % (condition, str_count))

            table_name = dict.get('name')

            command = "SELECT * FROM {0}".format(table_name)

            data = sql.query(command)
            # data = str(data)

            data = [{'ip': item[1], 'port': item[2]} for item in data]
            data = json.dumps(data, indent = 4)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(data)
        except Exception, e:
            log('server do get exception:%s' % str(e), logging.WARNING)
            self.send_response(404)

            # def runServer():
            # 	server = BaseHTTPServer.HTTPServer(('0.0.0.0', '8000'), Server)
            # 	server.serve_forever()


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), IpProxyServer)
    server.serve_forever()
