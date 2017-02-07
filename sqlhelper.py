#-*- coding: utf-8 -*-

import logging
import mysql.connector
import utils
import config

from singleton import Singleton


class SqlHelper(Singleton):
    def __init__(self):
        self.database_name = config.free_ipproxy_database
        self.init()

    def init(self):
        self.database = mysql.connector.connect(**config.database_config)
        self.cursor = self.database.cursor()

        self.create_database()
        self.database.database = self.database_name

    def create_database(self):
        try:
            command = 'CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARACTER SET \'utf8\' ' % self.database_name
            utils.log('sql helper create_database command:%s' % command)
            self.cursor.execute(command)
        except Exception, e:
            utils.log('SqlHelper create_database exception:%s' % str(e), logging.WARNING)

    def create_table(self, command):
        try:
            utils.log('sql helper create_table command:%s' % command)
            self.cursor.execute(command)
            self.database.commit()
        except Exception, e:
            utils.log('sql helper create_table exception:%s' % str(e), logging.WARNING)

    def insert_data(self, command, data):
        try:
            utils.log('insert_data command:%s, data:%s' % (command, data))

            self.cursor.execute(command, data)
            self.database.commit()
        except Exception, e:
            utils.log('sql helper insert_data exception msg:%s' % str(e), logging.WARNING)

    def execute(self, command):
        try:
            utils.log('sql helper execute command:%s' % command)
            data = self.cursor.execute(command)
            self.database.commit()
            return data
        except Exception, e:
            utils.log('sql helper execute exception msg:%s' % str(e))
            return None

    def query(self, command):
        try:
            utils.log('sql helper execute command:%s' % command)

            self.cursor.execute(command)
            data = self.cursor.fetchall()

            return data
        except Exception, e:
            utils.log('sql helper execute exception msg:%s' % str(e))
            return None

    def query_one(self, command):
        try:
            utils.log('sql helper execute command:%s' % command)

            self.cursor.execute(command)
            data = self.cursor.fetchone()

            return data
        except Exception, e:
            utils.log('sql helper execute exception msg:%s' % str(e))
            return None
