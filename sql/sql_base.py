#-*- coding: utf-8 -*-

class SqlBase(object):
    def __init__(self, **kwargs):
        pass

    def init_database(self, database_name):
        pass

    def init_proxy_table(self, table_name):
        pass

    def insert_proxy(self, table_name, proxy):
        pass

    def select_proxy(self, table_name, **kwargs):
        pass

    def update_proxy(self, table_name, proxy):
        pass

    def delete_proxy(self, table_name, proxy):
        pass

    def delete_old(self, table_name, day):
        pass

    def get_proxy_count(self, table_name):
        pass

    def get_proxy_ids(self, table_name):
        pass

    def get_proxy_with_id(self, table_name, id):
        pass

    def del_proxy_with_id(self, table_name, id):
        pass

    def del_proxy_with_ip(self, table_name, ip):
        pass

    def commit(self):
        pass
