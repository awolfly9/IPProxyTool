# -*- coding: utf-8 -*-

import logging
import os
import sys
import time
import utils
import aiohttp
from aiohttp import ClientSession
from sql.sql_manager import SqlManager
import config
import asyncio

TEST_URL='http://httpbin.org/ip'

async def test_connect(proxy,operator,mode=None):
    conn = aiohttp.TCPConnector(verify_ssl=False)
    async with ClientSession(connector=conn) as s:
        try:
            async with s.get(url=TEST_URL,proxy=proxy[2],
                             timeout=10,allow_redirects=False) as resp:
                page = await resp.text()
                if (resp.status != 200 or str(resp.url) != TEST_URL):
                    utils.log(('[INFO]#proxy:{ip} has been dropped\n'
                               '      #Reason:Abnormal url or return Code').format(ip=proxy[1]))
                    operator.del_proxy_with_id(config.free_ipproxy_table,proxy[0])
                    operator.del_proxy_with_id(config.httpbin_table,proxy[0])
                elif mode == 'add':
                    operator.insert_valid_proxy(id=proxy[0])
                else:
                    operator.update_valid_proxy(id=proxy[0])
                   
        except Exception as e:
            utils.log(('[INFO]#proxy:{ip} has been dropped\n'
                       '      #Reason:{msg}').format(ip=proxy[1],msg=str(e)))
            operator.del_proxy_with_id(config.free_ipproxy_table,proxy[0])
            operator.del_proxy_with_id(config.httpbin_table,proxy[0])
        finally:
            operator.commit()


def async_validator():
    utils.log('[INFO]#Loading ip proxies....60 sec left')
    time.sleep(60)
    proxy_factory = SqlManager()
    loop = asyncio.get_event_loop()
    def test_process(table_name,mode=None,limit=50):
        id_list = proxy_factory.get_proxy_ids(table_name) 
        if len(id_list) > 0:
            task_len = len(id_list)
            cur_id = 0
            for sig in range(0,task_len,limit):
                proxies = proxy_factory.get_proxies_info(table_name=table_name,
                                                         start_id=cur_id,
                                                         limit=limit)
                if len(proxies) == 0:
                    break
                cur_id = proxies[-1][0]
                proxies = [[proxy[0],proxy[1],'http://{}:{}'.format(proxy[1],proxy[2])] for proxy in proxies]
                tasks = [test_connect(proxy,proxy_factory,mode) for proxy in proxies]
                loop.run_until_complete(asyncio.wait(tasks))
    while True:
        utils.log('[INFO]Validator process started')
        utils.log('[INFO]Validator process:Verify mode start')
        test_process(config.httpbin_table)
        utils.log('[INFO]Validator process:Add mode start')
        test_process(config.free_ipproxy_table,mode='add')
        utils.log('[INFO]Validator process completed')
        time.sleep(300)


if __name__ == '__main__':
    if not os.path.exists('log'):
        os.makedirs('log')

    logging.basicConfig(
        filename = 'log/validator.log',
        format = '%(asctime)s: %(message)s',
        level = logging.INFO
    )
    async_validator()


