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

    def add_application(self, app_id, key, handler):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO apps (app_id, app_key, handler) " \
                  "VALUES ('{0}', '{1}', '{2}')".format(app_id, key, handler)
            cursor.execute(sql)
            self.connection.commit()

    def delete_application(self, app_id, key):
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM apps WHERE app_id = '{0}' AND key = '{1}'".format(app_id, key)
            cursor.execute(sql)
            self.connection.commit()

    def ping_native(self):
        self.logger.log('Pinging MYSQL.... (native)', 'MYSQL')
        self.connection.ping(True)

    def ping_alive(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT 1"
            cursor.execute(sql)
