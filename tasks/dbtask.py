# -*- coding: utf-8 -*-
from logger import Logger
import pymysql.cursors
import time
import config
import json
import threading


class DBTask:
    logger = None
    connection = None

    def __init__(self):
        self.logger = Logger()
        self.connect()

        # ping the database every x seconds
        timer = self.set_interval(self.ping, 30 * 60)

    def connect(self):
        self.connection = pymysql.connect(
            host=config.database['host'],
            user=config.database['user'],
            password=config.database['password'],
            db=config.database['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    def save(self, app_id, mqtt_msg):
        with self.connection.cursor() as cursor:
            self.logger.log('Saving message to DB...', 'TASK-MYSQL')
            json_raw = mqtt_msg.payload.decode("utf-8")
            data = json.loads(json_raw)

            # get best RSSI and it's gateway eui
            best_rssi = -1000
            best_gateway = ''
            best_snr = -1000
            best_received = ''
            # TODO: 'gateways' could be not exisiting
            if 'gateways' in data['metadata']:
                for gateway in data['metadata']['gateways']:
                    if gateway['rssi'] > best_rssi:
                        best_rssi = gateway['rssi']
                        best_gateway = gateway['gtw_id']
                        best_snr = gateway.get('snr', 0)
                        best_received = gateway['time']

            # strip dev_eui from topic string
            topic_splitted = mqtt_msg.topic.split('/')
            dev_eui = topic_splitted[2]

            if 'payload_fields' in data:
                payload_fields = json.dumps(data['payload_fields'])
            else:
                payload_fields = None

            sql = "INSERT INTO `data` (" \
                  "`app_id`, `dev_eui`," \
                  "`payload_raw`, `payload_fields`, `raw`," \
                  "`rssi`, `snr`, `gateway_eui`, `received`," \
                  "`created`) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor.execute("LOCK TABLES data WRITE, data_gateway WRITE")
            cursor.execute(sql, (app_id, dev_eui,
                                 data['payload_raw'], payload_fields, json_raw,
                                 best_rssi, best_snr, best_gateway, best_received,
                                 time.strftime('%Y-%m-%d %H:%M:%S')))
            lastid = cursor.lastrowid
            for gateway in data['metadata']['gateways']:
                g_rssi = gateway['rssi']
                g_gateway = gateway['gtw_id']
                g_snr = gateway.get('snr', 0)
                g_received = gateway['time']
                snr = 0
                received = 0
                sql_gateway = "INSERT INTO data_gateway (id,gateway_eui,rssi,snr,received) values (%s,%s,%s,%s,%s)"
                cursor.execute(sql_gateway, (lastid, g_gateway, g_rssi, g_snr, g_received))
            cursor.execute("UNLOCK TABLES")

        self.connection.commit()

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

    def set_interval(self, func, sec):
        def func_wrapper():
            self.set_interval(func, sec)
            func()
        t = threading.Timer(sec, func_wrapper)
        t.start()
        return t
