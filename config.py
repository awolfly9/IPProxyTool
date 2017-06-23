# coding=utf-8

DB_config = {
    # 'db_type': 'mongodb',
    'db_type': 'mysql',

    'mysql': {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'charset': 'utf8',
    },
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'password': '123456',
        'db': 1,
    },
    'mongodb':{
        'host': 'localhost',
        'port': 27017,
        'username': '',
        'password': '',
    }
}

database = 'ipproxy'
free_ipproxy_table = 'free_ipproxy'
httpbin_table = 'httpbin'

data_port = 8000
