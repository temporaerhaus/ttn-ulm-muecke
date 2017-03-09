# -*- coding: utf-8 -*-
from logger import Logger


class APITask:
    logger = None
    url = None
    data = None
    method = None

    def __init__(self):
        self.logger = Logger()

    def send(self, mqtt_msg):
        pass



