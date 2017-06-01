# -*- coding: utf-8 -*-
import pymysql.cursors
import config

_connection = None


def get_connection():
    global _connection
    if not _connection:
        _connection = pymysql.connect(
            host=config.database['host'],
            user=config.database['user'],
            password=config.database['password'],
            db=config.database['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    return _connection

