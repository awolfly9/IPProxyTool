#-*- coding: utf-8 -*-


from scrapy.http import Request
from validator import Validator
from config import *
from utils import *


class AssetStoreSpider(Validator):
    name = 'assetstore'

    def __init__(self, *a, **kwargs):
        super(AssetStoreSpider, self).__init__(*a, **kwargs)

        self.timeout = 10

        self.init()

    def start_requests(self):
        url = 'https://www.assetstore.unity3d.com/login'
        yield Request(
                url = url,
                headers = {
                    'Accept': 'application/json',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Host': 'www.assetstore.unity3d.com',
                    'Referer': 'https://www.assetstore.unity3d.com/en/',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 '
                                  'Firefox/50.0',
                    'X-Kharma-Version': '0',
                    'X-Requested-With': 'UnityAssetStore',
                    'X-Unity-Session': '26c4202eb475d02864b40827dfff11a14657aa41',
                },
                meta = {
                },
                dont_filter = True,
                callback = self.get_unity_version,
                errback = self.error_parse,
        )

    def get_unity_version(self, response):
        content = json.loads(response.body)
        self.log('unity content:%s' % response.body)

        unity_version = content.get('kharma_version', '')

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Host': 'www.assetstore.unity3d.com',
            'Referer': 'https://www.assetstore.unity3d.com/en/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
            'X-Kharma-Version': unity_version,
            'X-Requested-With': 'UnityAssetStore',
            'X-Unity-Session': '26c4202eb475d02864b40827dfff11a14657aa41',
        }

        count = get_table_length(self.sql, self.name)
        count_free = get_table_length(self.sql, free_ipproxy_table)

        for i in range(0, count + count_free):
            table = self.name if (i < count) else free_ipproxy_table

            proxy = get_proxy_info(self.sql, table, i)
            if proxy == None:
                continue

            url = 'https://www.assetstore.unity3d.com/api/en-US/content/overview/' + '368' + '.json'
            cur_time = time.time()
            yield Request(
                    url = url,
                    headers = headers,
                    meta = {
                        'cur_time': cur_time,
                        'download_timeout': self.timeout,
                        'proxy_info': proxy,
                        'table': table,
                        'id': proxy.get('id'),
                        'proxy': 'http://%s:%s' % (proxy.get('ip'), proxy.get('port')),
                    },
                    dont_filter = True,
                    callback = self.success_parse,
                    errback = self.error_parse,
            )

    def success_parse(self, response):
        self.log('success_parse proxy:%s' % str(response.meta.get('proxy')))

        filename = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S_%f')
        # self.save_page(filename, response.body)

        proxy = response.meta.get('proxy_info')
        speed = time.time() - response.meta.get('cur_time')
        table = response.meta.get('table')
        id = response.meta.get('id')

        self.log('speed:%s table:%s id:%s' % (speed, table, id))

        if table == self.name:
            if speed > self.timeout:
                command = get_delete_data_command(table, id)
                self.sql.execute(command)
            else:
                command = get_update_data_command(table, id, speed)
                self.sql.execute(command)
        else:
            if speed < self.timeout:
                command = get_insert_data_command(self.name)
                msg = (None, proxy.get('ip'), proxy.get('port'), proxy.get('country'), proxy.get('anonymity'),
                       proxy.get('https'), speed, proxy.get('source'), None)

                self.sql.insert_data(command, msg)