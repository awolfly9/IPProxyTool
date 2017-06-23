# -*- coding: utf-8 -*-

import json
import logging
import sys
import config

from proxy import Proxy
from sql import SqlManager
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/insert')
def insert():
    sql = SqlManager()
    name = request.args.get('name')
    proxy = Proxy()
    proxy.set_value(
        ip=request.args.get('ip'),
        port=request.args.get('port'),
        country=request.args.get('country', None),
        anonymity=request.args.get('anonymity', None),
        https=request.args.get('https', 'no'),
        speed=request.args.get('speed', -1),
        source=request.args.get('source', name),
    )

    result = sql.insert_proxy(name, proxy)
    data = {
        'result': result
    }

    return json.dumps(data, indent=4)


@app.route('/select')
def select():
    sql = SqlManager()
    name = request.args.get('name')
    anonymity = request.args.get('anonymity', '')
    https = request.args.get('https', '')
    order = request.args.get('order', 'speed')
    sort = request.args.get('sort', 'asc')
    count = request.args.get('count', 100)

    kwargs = {
        'anonymity': anonymity,
        'https': https,
        'order': order,
        'sort': sort,
        'count': count
    }
    result = sql.select_proxy(name, **kwargs)
    data = [{
        'ip': item.get('ip'), 'port': item.get('port'),
        'anonymity': item.get('anonymity'), 'https': item.get('https'),
        'speed': item.get('speed'), 'save_time': item.get('save_time', '')
    } for item in result]
    return json.dumps(data, indent=4)


@app.route('/delete')
def delete():
    sql = SqlManager()
    name = request.args.get('name')
    ip = request.args.get('ip')
    result = sql.del_proxy_with_ip(name, ip)
    data = {'result': result}

    return json.dumps(data, indent=4)
