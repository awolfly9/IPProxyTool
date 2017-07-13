# -*- coding: utf-8 -*-

import logging
import utils
import config
import pymysql

from proxy import Proxy
from sql.sql_base import SqlBase


class MySql(SqlBase):
    def __init__(self, **kwargs):
        super(MySql, self).__init__(**kwargs)

        self.conn = pymysql.connect(**kwargs)
        self.cursor = self.conn.cursor()

        try:
            self.conn.select_db(config.database)
        except:
            self.create_database(config.database)
            self.conn.select_db(config.database)

    def create_database(self, database_name):
        try:
            command = 'CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARACTER SET \'utf8\' ' % database_name
            logging.debug('mysql create_database command:%s' % command)
            self.cursor.execute(command)
            self.conn.commit()
        except Exception as e:
            logging.exception('mysql create_database exception:%s' % e)

    def init_database(self, database_name):
        try:
            command = 'CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARACTER SET \'utf8\' ' % database_name
            logging.debug('mysql create_database command:%s' % command)
            self.cursor.execute(command)
            self.conn.commit()
        except Exception as e:
            logging.exception('mysql create_database exception:%s' % e)

    def init_proxy_table(self, table_name):
        command = (
            "CREATE TABLE IF NOT EXISTS {} ("
            "`id` INT(8) NOT NULL AUTO_INCREMENT,"
            "`ip` CHAR(25) NOT NULL UNIQUE,"
            "`port` INT(4) NOT NULL,"
            "`country` TEXT DEFAULT NULL,"
            "`anonymity` INT(2) DEFAULT NULL,"
            "`https` CHAR(4) DEFAULT NULL ,"
            "`speed` FLOAT DEFAULT NULL,"
            "`source` CHAR(20) DEFAULT NULL,"
            "`save_time` TIMESTAMP NOT NULL,"
            "`vali_count` INT(5) DEFAULT 0,"
            "PRIMARY KEY(id)"
            ") ENGINE=InnoDB".format(table_name))

        self.cursor.execute(command)
        self.conn.commit()

    def insert_proxy(self, table_name, proxy):
        try:
            command = ("INSERT IGNORE INTO {} "
                       "(id, ip, port, country, anonymity, https, speed, source, save_time, vali_count)"
                       "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(table_name))

            data = (None, proxy.ip, proxy.port, proxy.country, proxy.anonymity,
                    proxy.https, proxy.speed, proxy.source, None, proxy.vali_count)

            self.cursor.execute(command, data)
            return True
        except Exception as e:
            logging.exception('mysql insert_proxy exception msg:%s' % e)
            return False

    def select_proxy(self, table_name, **kwargs):
        filter = {}
        for k, v in kwargs.items():
            if v != '':
                filter[k] = v

        try:
            command = "SELECT * FROM {name} WHERE anonymity LIKE '{anonymity}' AND https LIKE '{https}' ORDER BY " \
                      "{order} {sort} limit {count}". \
                format(name=table_name, anonymity=filter.get('anonymity', '%'),
                       https=filter.get('https', '%'), order=filter.get('order', 'save_time'),
                       sort=filter.get('sort', 'desc'), count=filter.get('count', 100))

            result = self.query(command)
            data = [{
                'ip': item[1], 'port': item[2], 'anonymity': item[4], 'https': item[5],
                'speed': item[6], 'save_time': str(item[8])
            } for item in result]
            return data
        except Exception as e:
            logging.exception('mysql select_proxy exception msg:%s' % e)
        return []

    def update_proxy(self, table_name, proxy):
        try:
            command = "UPDATE {table_name} set https='{https}', speed={speed}, " \
                      "vali_count={vali_count}, anonymity = {anonymity},save_time={save_time} " \
                      "where id={id};".format(
                table_name=table_name, https=proxy.https,
                speed=proxy.speed, id=proxy.id, vali_count=proxy.vali_count, anonymity=proxy.anonymity,
                save_time='NOW()')
            logging.debug('mysql update_proxy command:%s' % command)
            self.cursor.execute(command)
        except Exception as e:
            logging.exception('mysql update_proxy exception msg:%s' % e)

    def delete_proxy(self, table_name, proxy):
        self.del_proxy_with_id(table_name=table_name, id=proxy.id)

    def delete_old(self, table_name, day):
        try:
            command = "DELETE FROM {table} where save_time < SUBDATE(NOW(), INTERVAL {day} DAY)".format(
                table=config.free_ipproxy_table, day=day)

            self.cursor.execute(command)
            self.commit()
        except Exception as e:
            logging.exception('mysql delete_old exception msg:%s' % e)

    def get_proxy_count(self, table_name):
        try:
            command = "SELECT COUNT(*) from {}".format(table_name)
            count, = self.query_one(command)
            logging.debug('mysql get_proxy_count count:%s' % count)
            return count
        except Exception as e:
            logging.exception('mysql get_proxy_count exception msg:%s' % e)

        return 0

    def get_proxy_ids(self, table_name):
        ids = []
        try:
            command = "SELECT id from {}".format(table_name)
            result = self.query(command)
            ids = [item[0] for item in result]
        except Exception as e:
            logging.exception('mysql get_proxy_ids exception msg:%s' % e)

        return ids

    def get_proxy_with_id(self, table_name, id):
        proxy = Proxy()
        try:
            command = "SELECT * FROM {0} WHERE id=\'{1}\'".format(table_name, id)
            result = self.query_one(command)
            if result != None:
                # data = {
                #     'id': result[0],
                #     'ip': result[1],
                #     'port': result[2],
                #     'country': result[3],
                #     'anonymity': result[4],
                #     'https': result[5],
                #     'speed': result[6],
                #     'source': result[7],
                #     'save_time': result[8],
                #     'vali_count': result[9],
                # }
                proxy = Proxy()
                proxy.set_value(
                    ip=result[1],
                    port=result[2],
                    country=result[3],
                    anonymity=result[4],
                    https=result[5],
                    speed=result[6],
                    source=result[7],
                    vali_count=result[9])
                proxy.id = result[0]
                proxy.save_time = result[8]
        except Exception as e:
            logging.exception('mysql get_proxy_ids exception msg:%s' % e)

        return proxy

    def del_proxy_with_id(self, table_name, id):
        res = False
        try:
            command = "DELETE FROM {0} WHERE id={1}".format(table_name, id)
            self.cursor.execute(command)
            res = True
        except Exception as e:
            logging.exception('mysql get_proxy_ids exception msg:%s' % e)

        return res

    def del_proxy_with_ip(self, table_name, ip):
        res = False
        try:
            command = "DELETE FROM {0} WHERE ip='{1}'".format(table_name, ip)
            self.cursor.execute(command)
            self.commit()
            res = True
        except Exception as e:
            logging.exception('mysql del_proxy_with_ip exception msg:%s' % e)

        return res

    def create_table(self, command):
        try:
            logging.debug('mysql create_table command:%s' % command)
            x = self.cursor.execute(command)
            self.conn.commit()
            return x
        except Exception as e:
            logging.exception('mysql create_table exception:%s' % e)

    def insert_data(self, command, data, commit=False):
        try:
            logging.debug('mysql insert_data command:%s, data:%s' % (command, data))
            x = self.cursor.execute(command, data)
            if commit:
                self.conn.commit()
            return x
        except Exception as e:
            logging.debug('mysql insert_data exception msg:%s' % e)

    def commit(self):
        self.conn.commit()

    def execute(self, command, commit=True):
        try:
            logging.debug('mysql execute command:%s' % command)
            data = self.cursor.execute(command)
            if commit:
                self.conn.commit()
            return data
        except Exception as e:
            logging.exception('mysql execute exception msg:%s' % e)
            return None

    def query(self, command, commit=False):
        try:
            logging.debug('mysql execute command:%s' % command)

            self.cursor.execute(command)
            data = self.cursor.fetchall()
            if commit:
                self.conn.commit()
            return data
        except Exception as e:
            logging.exception('mysql execute exception msg:%s' % e)
            return None

    def query_one(self, command, commit=False):
        try:
            logging.debug('mysql execute command:%s' % command)

            self.cursor.execute(command)
            data = self.cursor.fetchone()
            if commit:
                self.conn.commit()

            return data
        except Exception as e:
            logging.debug('mysql execute exception msg:%s' % str(e))
            return None
