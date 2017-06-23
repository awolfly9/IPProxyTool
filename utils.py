#-*- coding: utf-8 -*-

import logging
import os
import re
import subprocess
import traceback
import time
import datetime


# 自定义的日志输出
def log(msg, level = logging.DEBUG):
    logging.log(level, msg)
    print('%s [%s], msg:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), level, msg))

    if level == logging.WARNING or level == logging.ERROR:
        for line in traceback.format_stack():
            print(line.strip())

        for line in traceback.format_stack():
            logging.log(level, line.strip())


# 服务器使用，清理端口占用
def kill_ports(ports):
    for port in ports:
        log('kill %s start' % port)
        popen = subprocess.Popen('lsof -i:%s' % port, shell = True, stdout = subprocess.PIPE)
        (data, err) = popen.communicate()
        log('data:\n%s  \nerr:\n%s' % (data, err))

        pattern = re.compile(r'\b\d+\b', re.S)
        pids = re.findall(pattern, data.decode())

        log('pids:%s' % str(pids))

        for pid in pids:
            if pid != '' and pid != None:
                try:
                    log('pid:%s' % pid)
                    popen = subprocess.Popen('kill -9 %s' % pid, shell = True, stdout = subprocess.PIPE)
                    (data, err) = popen.communicate()
                    log('data:\n%s  \nerr:\n%s' % (data, err))
                except Exception as e:
                    log('kill_ports exception:%s' % e)

        log('kill %s finish' % port)

    time.sleep(1)


# 创建文件夹
def make_dir(dir):
    log('make dir:%s' % dir)
    if not os.path.exists(dir):
        os.makedirs(dir)
