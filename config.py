# coding=utf-8

# 验证 URL
#VALIDATOR_URL = 'https://www.assetstore.unity3d.com/'
import json

VALIDATOR_URL = 'https://www.assetstore.unity3d.com/login'

# 验证检查 文本
#VALIDATOR_TEXT = 'assetstore'
VALIDATOR_TEXT = 'kharma_version'

# 超时时间
WAIT_TIME = 20 * 60

database_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
}

free_ipproxy_database = 'ipproxy'
free_ipproxy_table = 'free_ipproxy'

baidu_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Host': 'www.baidu.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
}

validator_ipproxy = [
    {
        'table': 'baidu',
        'url': 'https://www.baidu.com/',
        'success': '百度一下，你就知道',
        'headers': json.dumps(baidu_headers)
    },
    # {
    #     'table': 'assetstore',
    #     'url': 'https://www.assetstore.unity3d.com/login',
    #     'success': 'kharma_version',
    # },
    # {
    #     'table': 'github',
    #     'url': 'https://github.com/',
    #     'success': 'github',
    # },
    # {
    #     'table': 'steam',
    #     'url': 'http://store.steampowered.com/',
    #     'success': 'store',
    # },
    # {
    #     'table': 'google',
    #     'url': 'https://www.google.com/?gws_rd=ssl',
    #     'success': 'Google Search',
    # },
]

'''
7 error_parse value:[<twisted.python.failure.Failure twisted.internet.error.ConnectionLost: Connection to the other
side was lost in a non-clean fashion.>]
630 error_parse value:User timeout caused connection failure.
9 error_parse value:[<twisted.python.failure.Failure twisted.internet.error.ConnectionDone: Connection was closed
cleanly.>]
76 error_parse value:User timeout caused connection failure: Getting http://store.steampowered.com/ took longer than
10 seconds..
193 error_parse value:Connection was refused by other side: 61: Connection refused.
246 error_parse value:User timeout caused connection failure:
206 error_parse value:Ignoring non-200 response
245 error_parse value:Could not open CONNECT tunnel with proxy
10 error_parse value:No route to host: 51: Network is unreachable.
2 error_parse value:[<twisted.python.failure.Failure OpenSSL.SSL.Error:

'''
