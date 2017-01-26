# -*- coding: utf-8 -*-
from time import strftime, localtime


class Logger:
    with_time = True

    def __init__(self):
        pass

    def log(self, msg, tag='INFO'):
        now = strftime("%H:%M:%S", localtime())
        print((now+' ' if self.with_time else '') + '['+tag+'] ' + msg)
