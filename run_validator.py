# -*- coding: utf-8 -*-

import logging
import os
import subprocess
import sys
import time
import scrapydo
import utils
from importlib import import_module

VALIDATORS = {'HttpBinSpider' :'ipproxytool.spiders.validator.httpbin',
            # 'DoubanSpider':'ipproxytool.spiders.validator.douban',
            # 'AssetStoreSpider':'ipproxytool.spiders.validator.assetstore',
            # 'GatherSpider' :'ipproxytool.spiders.validator.gather',
            # 'HttpBinSpider' :'ipproxytool.spiders.validator.httpbin',
            # 'SteamSpider' :'ipproxytool.spiders.validator.steam',
            # 'BossSpider' :'ipproxytool.spiders.validator.boss',
            # 'LagouSpider' :'ipproxytool.spiders.validator.lagou',
            # 'LiepinSpider' :'ipproxytool.spiders.validator.liepin',
            # 'JDSpider' :'ipproxytool.spiders.validator.jd',
            # 'BBSSpider' :'ipproxytool.spiders.validator.bbs',
            # 'ZhiLianSpider' :'ipproxytool.spiders.validator.zhilian',
            # 'AmazonCnSpider' :'ipproxytool.spiders.validator.amazoncn',
              }

scrapydo.setup()

def validator():
     
    process_list = []
    for item, path in VALIDATORS.items():
        module = import_module(path)
        validator = getattr(module,item)
        popen = subprocess.Popen(['python', 'run_spider.py', validator.name], shell=False)
        data = {
            'name': validator.name,
            'popen': popen,
        }
        process_list.append(data)

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
                p = subprocess.Popen(['python', 'run_spider.py', name], shell = False)
                data = {
                    'name': name,
                    'popen': p,
                }
                process_list.append(data)
                time.sleep(1)
                break


if __name__ == '__main__':
    os.chdir(sys.path[0])

    if not os.path.exists('log'):
        os.makedirs('log')

    logging.basicConfig(
        filename = 'log/validator.log',
        format = '%(asctime)s: %(message)s',
        level = logging.DEBUG
    )

    validator()
