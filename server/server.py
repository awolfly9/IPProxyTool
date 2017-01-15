# coding=utf-8

import logging
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json
import urllib
import urlparse
from SqlHelper import SqlHelper
from utils import *
from config import *


class Server(BaseHTTPRequestHandler):
    # def __init__(self, request, client_address, server):
    #     BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
    #     self.protocol_version = 'HTTP/1.1'
    #
    #     self.sql = SqlHelper()

    #http://127.0.0.1:8000/?type=1&count=10&country=%E4%B8%AD%E5%9B%BD
    #http://127.0.0.1:8000/?type=1&count=10&country=中国
    #http://127.0.0.1:8000
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
                else:
                    log('没有处理的参数:%s 值为:%s' % (key, value), logging.WARNING)

            log('condition:%s, count:%s' % (condition, str_count))

            command = "select * from {}".format(free_ipproxy_table)

            data = sql.query(command)
            data = str(data)

            #
            # results = sql.select(condition, str_count)
            # data = [{'ip': item[0], 'port': item[1]} for item in results]
            # data = json.dumps(data, indent = 4)

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
    server = HTTPServer(('0.0.0.0', 8000), Server)
    server.serve_forever()
