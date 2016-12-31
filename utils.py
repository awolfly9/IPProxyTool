#-*- coding: utf-8 -*-

import logging


def log(msg, level = logging.DEBUG):
    logging.log(level, msg)
    print('level:%s, msg:%s' % (level, msg))
