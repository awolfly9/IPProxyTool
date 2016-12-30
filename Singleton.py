#-*- coding: utf-8 -*-

import threading

class Singleton(object):

    lock = threading.Lock()

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            Singleton.lock.acquire(True)
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
            cls.is_init = False
            Singleton.lock.release()
        return cls._instance

