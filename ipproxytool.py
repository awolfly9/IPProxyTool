# coding=utf-8

import logging
import os
import sys
import subprocess
import run_validator

if __name__ == '__main__':

    # 进入当前项目目录
    os.chdir(sys.path[0])

    if not os.path.exists('log'):
        os.makedirs('log')

    logging.basicConfig(
            filename = 'log/ipproxy.log',
            format = '%(asctime)s: %(message)s',
            level = logging.DEBUG
    )

    subprocess.Popen(['python', 'run_crawl_proxy.py'])
    subprocess.Popen(['python', 'run_server.py'])

    run_validator.validator()


