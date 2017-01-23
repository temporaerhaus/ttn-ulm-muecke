# -*- coding: utf-8 -*-
import random
from time import sleep
import database


class Subscriber:
    client = None
    database = None
    app = None

    failed_apps = {}

    min_sleep_time = 10
    max_sleep_time = 60

    def __init__(self, database, app, client):
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
        #print('connected')
        subscribe_path = '+/devices/+/up'
        print('[INFO] Subscribing to app '+self.app['app_id']+' on topic ' + subscribe_path)
        self.client.subscribe(subscribe_path)

    def on_message(self, client, userdata, msg):
        #print('got message')
        print('[INFO] Message on topic ' + msg.topic + '\n' + str(msg.payload))
        self.database.save(self.app['id'], msg)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print('[RECONNECT] Unexcepted disconnect from app ' + str(userdata))
            random.seed()
            sleep_duration = random.randint(self.min_sleep_time, self.max_sleep_time)
            print('[RECONNECT] Sleeping for ' + str(sleep_duration) + 's...')
            sleep(sleep_duration)

            db = database.Database()
            self.app = db.get_application(self.id)
            if self.app:
                print('[RECONNECT] Sleep finished. Got new app credentials. Retrying connection...')
                self.client.username_pw_set(self.app['app_id'], self.app['app_key'])
                self.client.connect_async('eu.thethings.network', 1883, 60)

