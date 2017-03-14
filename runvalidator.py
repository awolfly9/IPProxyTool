#-*- coding: utf-8 -*-

import logging
import os
import subprocess
import sys
import time
import scrapydo
import utils
import datetime

from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from ipproxytool.spiders.validator.douban import DoubanSpider
from ipproxytool.spiders.validator.assetstore import AssetStoreSpider
from ipproxytool.spiders.validator.gather import GatherSpider
from ipproxytool.spiders.validator.httpbin import HttpBinSpider
from ipproxytool.spiders.validator.steam import SteamSpider
from ipproxytool.spiders.validator.boss import BossSpider
from ipproxytool.spiders.validator.lagou import LagouSpider
from ipproxytool.spiders.validator.liepin import LiepinSpider

scrapydo.setup()

if __name__ == '__main__':
    os.chdir(sys.path[0])

    reload(sys)
    sys.setdefaultencoding('utf-8')

    if not os.path.exists('log'):
        os.makedirs('log')

    logging.basicConfig(
            filename = 'log/validator.log',
            format = '%(asctime)s: %(message)s',
            level = logging.DEBUG
    )

    validators = [
        HttpBinSpider,  # 必须
        LagouSpider,
        BossSpider,
        LiepinSpider,
    ]

    process_list = []
    for validator in validators:
        popen = subprocess.Popen(['python', 'runscrapy.py', validator.name], shell = False)
        data = {
            'name': validator.name,
            'popen': popen,
        }
        process_list.append(data)

    utils.log(process_list)

    while True:
        time.sleep(60)
        for process in process_list:
            popen = process.get('popen', None)
            utils.log('name:%s poll:%s' % (process.get('name'), popen.poll()))

            #  检测结束进程，如果有结束进程，重新开启
            if popen != None and popen.poll() == 0:
                name = process.get('name')
                utils.log('%(name)s spider finish...\n' % {'name': name})

                process_list.remove(process)

                p = subprocess.Popen(['python', 'runscrapy.py', name], shell = False)
                data = {
                    'name': name,
                    'popen': p,
                }
                process_list.append(data)

                time.sleep(1)
                break
