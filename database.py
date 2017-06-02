# -*- coding: utf-8 -*-
import pymysql.cursors
import config
from logger import Logger


class Database:
    connection = None
    logger = None

    def __init__(self):
        self.logger = Logger()
        self.connect()

    def connect(self):
        self.connection = pymysql.connect(
            host=config.database['host'],
            user=config.database['user'],
            password=config.database['password'],
            db=config.database['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
        self.logger.log('Connected.', 'MYSQL')

    def get_connection(self):
        return self.connection

    def get_applications(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM `apps`"
            cursor.execute(sql)
            results = cursor.fetchall()
            return results

    def get_application(self, app_id):
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM `apps` WHERE id = " + str(app_id)
            cursor.execute(sql)
            results = cursor.fetchall()
            return results[0]

    def ping(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT 1"
            cursor.execute(sql)
