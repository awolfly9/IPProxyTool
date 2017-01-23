# coding=utf-8

import BaseHTTPServer
import Queue
import logging
import threading
import sys

import time

from Server import Server
from Validator import Validator
from SpiderManager import SpiderManager
from sqlhelper import SqlHelper
from KillPort import kill_ports
from scrapy import cmdline
import subprocess
from QueueMng import queue_mng


class IPProxyTool(object):
    def __init__(self):
        logging.basicConfig(
                filename = 'log/spider.log',
                filemode = 'a',
                format = 'Spider:%(levelname)s:%(name)s:%(message)s',
                level = logging.DEBUG,
        )

        self.queue = queue_mng.queue

    def run_spider(self):
        spider = SpiderManager(self.queue)
        spider.run()

    def run_validator(self):
        validator = Validator(self.queue)
        validator.run()

    def run_server(self):
        server = BaseHTTPServer.HTTPServer(('0.0.0.0', 8000), Server)
        server.serve_forever()

if __name__ == '__main__':
    #解决编码问题
    reload(sys)
    sys.setdefaultencoding('utf-8')

    ports = ['8000']
    kill_ports(ports)

    time.sleep(1)

    tool = IPProxyTool()

    # 开启多个工作线程
    spider = threading.Thread(target = tool.run_spider)
    validator = threading.Thread(target = tool.run_validator)
    server = threading.Thread(target = tool.run_server)

    spider.start()
    #validator.start()
    # server.start()

    cmdline.execute('scrapy crawl test'.split())


