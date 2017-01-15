#-*- coding: utf-8 -*-

import logging
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


def kill_ports(ports):
    for port in ports:
        log('kill %s start' % port)
        popen = subprocess.Popen('lsof -i:%s' % port, shell = True, stdout = subprocess.PIPE)
        (data, err) = popen.communicate()
        log('data:\n%s  \nerr:\n%s' % (data, err))

        pattern = re.compile(r'\b\d+\b', re.S)
        pids = re.findall(pattern, data)

        log('pids:%s' % str(pids))

        for pid in pids:
            if pid != '' and pid != None:
                try:
                    log('pid:%s' % pid)
                    popen = subprocess.Popen('kill -9 %s' % pid, shell = True, stdout = subprocess.PIPE)
                    (data, err) = popen.communicate()
                    log('data:\n%s  \nerr:\n%s' % (data, err))
                except Exception, e:
                    log('kill_ports exception:%s' % e)

        log('kill %s finish' % port)

    time.sleep(1)


def get_create_table_command(table_name):
    command = (
        "CREATE TABLE IF NOT EXISTS {} ("
        "`id` INT(8) NOT NULL AUTO_INCREMENT,"
        "`ip` CHAR(25) NOT NULL UNIQUE,"
        "`port` INT(4) NOT NULL,"
        "`country` TEXT DEFAULT NULL,"
        "`anonymity` INT(2) DEFAULT NULL,"
        "`https` CHAR(4) DEFAULT NULL ,"
        "`speed` FLOAT DEFAULT NULL,"
        "`save_time` TIMESTAMP NOT NULL,"
        "PRIMARY KEY(id)"
        ") ENGINE=InnoDB".format(table_name))

    return command


def get_insert_data_command(table_name):
    command = ("INSERT IGNORE INTO {} "
               "(id, ip, port, country, anonymity, https, speed, save_time)"
               "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)".format(table_name))

    return command
