#-*- coding: utf-8 -*-

import logging
import utils
import config
import pymysql


class SqlHelper(object):
    def __init__(self):
        self.conn = pymysql.connect(**config.database_config)
        self.cursor = self.conn.cursor()

        try:
            self.conn.select_db(config.database)
        except:
            self.create_database()
            self.conn.select_db(config.database)

    def create_database(self):
        try:
            command = 'CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARACTER SET \'utf8\' ' % config.database
            utils.log('sql helper create_database command:%s' % command)
            self.cursor.execute(command)
            self.conn.commit()
        except Exception, e:
            utils.log('SqlHelper create_database exception:%s' % str(e), logging.WARNING)

    def create_table(self, command):
        try:
            utils.log('sql helper create_table command:%s' % command)
            x = self.cursor.execute(command)
            self.conn.commit()
            return x
        except Exception, e:
            utils.log('sql helper create_table exception:%s' % str(e), logging.WARNING)

    def insert_data(self, command, data, commit = False):
        try:
            utils.log('sql helper insert_data command:%s, data:%s' % (command, data))
            x = self.cursor.execute(command, data)
            if commit:
                self.conn.commit()
            return x
        except Exception, e:
            utils.log('sql helper insert_data exception msg:%s' % str(e), logging.WARNING)

    def commit(self):
        self.conn.commit()

    def execute(self, command, commit = True):
        try:
            utils.log('sql helper execute command:%s' % command)
            data = self.cursor.execute(command)
            if commit:
                self.conn.commit()
            return data
        except Exception, e:
            utils.log('sql helper execute exception msg:%s' % str(e))
            return None

    def query(self, command, commit = False):
        try:
            utils.log('sql helper execute command:%s' % command)

            self.cursor.execute(command)
            data = self.cursor.fetchall()
            if commit:
                self.conn.commit()
            return data
        except Exception, e:
            utils.log('sql helper execute exception msg:%s' % str(e))
            return None

    def query_one(self, command, commit = False):
        try:
            utils.log('sql helper execute command:%s' % command)

            self.cursor.execute(command)
            data = self.cursor.fetchone()
            if commit:
                self.conn.commit()

            return data
        except Exception, e:
            utils.log('sql helper execute exception msg:%s' % str(e))
            return None
