# -*- coding: utf-8 -*-
import random
from time import sleep
from logger import Logger
import database
import json


class Subscriber:
    logger = None
    client = None
    db = None
    app = None

    failed_apps = {}
    handlers = {
        '1': ('ttn-handler-eu', 'eu.thethings.network'),
        '2': ('cortex-media (TTN Ulm)', 'ttn.cortex-media.de')
    }
    handler = handlers['1'][1]

    min_sleep_time = 10
    max_sleep_time = 60

    log_with_payload = False

    def __init__(self, app, client):
        self.logger = Logger()
        self.db = database.Database()
        self.app = app
        self.id = app['id']
        self.client = client

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        self.client.username_pw_set(self.app['app_id'], self.app['app_key'])

        settings_raw = self.app['settings']
        if settings_raw:
            settings = json.loads(settings_raw)
            if 'handler' in settings:
                handler_id = settings['handler']
                self.handler = self.handlers[handler_id][1]
            else:
                self.handler = self.handlers['1'][1]
        else:
            self.handler = self.handlers['1'][1]

        self.client.connect_async(self.handler, 1883, 60)

    def on_connect(self, client, userdata, flags, rc):
        subscribe_path = '+/devices/+/up'
        self.logger.log('Subscribing to app '+self.app['app_id']+' on topic ' + subscribe_path + ' on hadler ' + self.handler)
        self.client.subscribe(subscribe_path)

    def on_message(self, client, userdata, msg):
        self.logger.log('Message on topic ' + msg.topic + (str('\n'+msg.payload) if self.log_with_payload else ''))
        self.db.save(self.app['id'], msg)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.logger.log('Unexcepted disconnect from app ' + str(userdata), 'RECONNECT')
            random.seed()
            sleep_duration = random.randint(self.min_sleep_time, self.max_sleep_time)
            self.logger.log('Sleeping for ' + str(sleep_duration) + 's...', 'RECONNECT')
            sleep(sleep_duration)

            self.app = self.db.get_application(self.id)
            if self.app:
                self.logger.log('Sleep finished. Got new app credentials. Retrying connection...', 'RECONNECT')
                self.client.username_pw_set(self.app['app_id'], self.app['app_key'])
                self.client.connect_async(self.handler, 1883, 60)

