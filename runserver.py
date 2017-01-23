#-*- coding: utf-8 -*-

import BaseHTTPServer

from server.ipproxyserver import IpProxyServer
from utils import kill_ports

if __name__ == '__main__':
    kill_ports(['8000'])

    server = BaseHTTPServer.HTTPServer(('0.0.0.0', 8000), IpProxyServer)
    server.serve_forever()
