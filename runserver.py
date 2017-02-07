#-*- coding: utf-8 -*-

import config

from server import dataserver
from utils import kill_ports

if __name__ == '__main__':
    kill_ports([config.data_port])

    dataserver.start_api_server()
