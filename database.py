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

    def save(self, app_eui, payload_decoded, raw):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO `data` (`appEUI`, `payload`, `raw`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (app_eui, payload_decoded, raw))

        self.connection.commit()
