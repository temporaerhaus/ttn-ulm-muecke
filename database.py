# -*- coding: utf-8 -*-
import base64
import pymysql.cursors
import time
import config
import json


class Database:
    connection = None

    def __init__(self):
        self.connection = pymysql.connect(
            host=config.database['host'],
            user=config.database['user'],
            password=config.database['password'],
            db=config.database['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    def save(self, app_id, mqtt_msg):
        with self.connection.cursor() as cursor:

            json_raw = mqtt_msg.payload.decode("utf-8")
            data = json.loads(json_raw)

            # get best RSSI and it's gateway eui
            best_rssi = -1000
            best_gateway = ''
            best_snr = -1000
            best_received = ''
            for gateway in data['metadata']['gateways']:
                if gateway['rssi'] > best_rssi:
                    best_rssi = gateway['rssi']
                    best_gateway = gateway['gtw_id']
                    best_snr = gateway['snr']
                    best_received = gateway['time']

            # strip dev_eui from topic string
            topic_splitted = mqtt_msg.topic.split('/')
            dev_eui = topic_splitted[2]

            sql = "INSERT INTO `data` (" \
                  "`app_id`, `dev_eui`," \
                  "`payload_raw`, `payload_fields`, `raw`," \
                  "`rssi`, `snr`, `gateway_eui`, `received`," \
                  "`created`) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (app_id, dev_eui,
                                 data['payload_raw'], json.dumps(data['payload_fields']), json_raw,
                                 best_rssi, best_snr, best_gateway, best_received,
                                 time.strftime('%Y-%m-%d %H:%M:%S')))

        self.connection.commit()

    def get_applications(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM `apps`"
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
