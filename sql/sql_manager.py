# -*- coding: utf-8 -*-

import config

from sql.sql_base import SqlBase


class SqlManager(object):
    def __init__(self):
        db_type = config.DB_config.get('db_type', 'mysql')
        db_config = config.DB_config.get(db_type)

        if db_type == 'mysql':
            from sql.mysql import MySql
            self.sql = MySql(**db_config)
        elif db_type == 'redis':
            pass
        elif db_type == 'sqlite':
            pass
        elif db_type == 'mongodb':
            from sql.mongodb import Mongodb
            self.sql = Mongodb(**db_config)
        else:  # default mysql
            from sql.mysql import MySql
            self.sql = MySql(**config.DB_config.get('db_type'))

    def init_database(self, database_name):
        pass

    def init_proxy_table(self, table_name):
        return self.sql.init_proxy_table(table_name)

    def insert_proxy(self, table_name, proxy):
        return self.sql.insert_proxy(table_name, proxy)

    def select_proxy(self, table_name, **kwargs):
        return self.sql.select_proxy(table_name, **kwargs)

    def update_proxy(self, table_name, proxy):
        return self.sql.update_proxy(table_name, proxy)

    def delete_proxy(self, table_name, proxy):
        return self.sql.delete_proxy(table_name, proxy)

    def delete_old(self, table_name, day):
        return self.sql.delete_old(table_name, day)

    def get_proxy_count(self, table_name):
        return self.sql.get_proxy_count(table_name = table_name)

    def get_proxy_ids(self, table_name):
        return self.sql.get_proxy_ids(table_name = table_name)

    def get_proxy_with_id(self, table_name, id):
        return self.sql.get_proxy_with_id(table_name = table_name, id = id)

    def del_proxy_with_id(self, table_name, id):
        return self.sql.del_proxy_with_id(table_name = table_name, id = id)

    def del_proxy_with_ip(self, table_name, ip):
        return self.sql.del_proxy_with_ip(table_name = table_name, ip = ip)

    def commit(self):
        return self.sql.commit()
