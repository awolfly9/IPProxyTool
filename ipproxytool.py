# coding=utf-8

import logging
import os
import sys
import subprocess
import run_validator
import run_validator_async

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
    
    if 'async' in sys.argv: 
        run_validator_async.async_validator()
    else:
        run_validator.validator()



