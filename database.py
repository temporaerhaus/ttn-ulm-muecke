# -*- coding: utf-8 -*-
import pymysql.cursors


class Database:
    connection = None

    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='muecke',
            password='muecke',
            db='muecke',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    def save(self, app_id, dev_eui, payload_decoded, raw):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO `data` (`app_id`, `dev_eui`, `payload`, `raw`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (app_id, dev_eui, payload_decoded, raw))

        self.connection.commit()

    def get_applications(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM `apps`"
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
