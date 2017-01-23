#-*- coding: utf-8 -*-

from scrapy.spiders import Spider
from sqlhelper import SqlHelper
from utils import *


class BaseValidator(Spider):
    name = 'base'

    def __init__(self, name = None, **kwargs):
        super(BaseValidator, self).__init__(name, **kwargs)
        self.sql = SqlHelper()
        self.dir_log = 'log/validator/validator'
        self.table_name = 'validator'
        self.timeout = 10

    def init(self):
        make_dir(self.dir_log)

        command = get_create_table_command(self.table_name)
        self.sql.create_table(command)

    def save_page(self, filename, data):
        with open('%s/%s.html' % (self.dir_log, filename), 'w') as f:
            f.write(data)
            f.close()
