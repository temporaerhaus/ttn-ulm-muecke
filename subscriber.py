# -*- coding: utf-8 -*-
import random
from time import sleep
from logger import Logger


class Subscriber:
    logger = None
    client = None
    database = None
    app = None

    failed_apps = {}

    min_sleep_time = 10
    max_sleep_time = 60

    log_with_payload = False

    def __init__(self, database, app, client):
        self.logger = Logger()
        self.database = database
        self.app = app
        self.id = app['id']
        self.client = client

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        self.client.username_pw_set(self.app['app_id'], self.app['app_key'])
        self.client.connect_async('eu.thethings.network', 1883, 60)

    def on_connect(self, client, userdata, flags, rc):
        subscribe_path = '+/devices/+/up'
        self.logger.log('Subscribing to app '+self.app['app_id']+' on topic ' + subscribe_path)
        self.client.subscribe(subscribe_path)

    def on_message(self, client, userdata, msg):
        self.logger.log('Message on topic ' + msg.topic + (str('\n'+msg.payload) if self.log_with_payload else ''))
        self.database.save(self.app['id'], msg)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.logger.log('Unexcepted disconnect from app ' + str(userdata), 'RECONNECT')
            random.seed()
            sleep_duration = random.randint(self.min_sleep_time, self.max_sleep_time)
            self.logger.log('Sleeping for ' + str(sleep_duration) + 's...', 'RECONNECT')
            sleep(sleep_duration)

            self.app = self.database.get_application(self.id)
            if self.app:
                self.logger.log('Sleep finished. Got new app credentials. Retrying connection...', 'RECONNECT')
                self.client.username_pw_set(self.app['app_id'], self.app['app_key'])
                self.client.connect_async('eu.thethings.network', 1883, 60)

