# coding=utf-8
import logging
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json
import urllib
import urlparse
from SqlHelper import SqlHelper


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
        self.str_count = ''
        self.condition = ''

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

            print('dict:%s' % str(dict))

            i = 0
            for key, value in dict.items():
                print('key:%s, value:%s' % (key, value))
                if key == 'type':
                    cond = 'anonymity="' + value + '"'
                    if i > 0:
                        self.condition = self.condition + ' And '
                    self.condition = self.condition + cond
                    i = i + 1
                elif key == 'country':
                    cond = 'country="' + value.decode('utf-8') + '"'
                    if i > 0:
                        self.condition = self.condition + ' And '

                    self.condition = self.condition + cond
                    i = i + 1
                elif key == 'count':
                    self.str_count = 'limit ' + value
                else:
                    logging.warning('没有处理的参数:%s 值为:%s' % (key, value))
                    print('没有处理的参数:%s 值为:%s' % (key, value))

            print('condition:%s, count:%s' % (self.condition, self.str_count))
            results = sql.select(self.condition, self.str_count)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(results, indent = 4))
        except Exception, e:
            logging.warning(str(e))
            self.send_response(404)

    # def runServer():
    # 	server = BaseHTTPServer.HTTPServer(('0.0.0.0', '8000'), Server)
    # 	server.serve_forever()

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), Server)
    server.serve_forever()