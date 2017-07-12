# -*- coding: utf-8 -*-
import random
from time import sleep
import importlib
from logger import Logger
import config
import database
import threading


class Subscriber:
    logger = None
    client = None
    db = None
    app = None

    failed_apps = {}
    handlers = {
        '1': ('ttn-handler-eu (TTN)', 'eu.thethings.network'),
        '2': ('Cortex Media (TTN Ulm)', 'ttn.cortex-media.de')
    }
    handler = handlers['1'][1]

    min_sleep_time = 5
    max_sleep_time = 20

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

        if self.app['handler']:
            self.handler = self.app['handler']
        else:
            self.handler = self.handlers['1'][0]

        #self.client.tls_set('certs/ca.pem')
        #self.client.tls_insecure_set(True)
        self.client.connect_async(self.handler, 1883, 60)

        # ping the database every x seconds
        timer = self.set_interval(self.db.ping_native, 60*15)

    def on_connect(self, client, userdata, flags, rc):
        subscribe_path = '+/devices/+/up'
        self.logger.log('Subscribing to app '+self.app['app_id']+' on topic ' + subscribe_path + ' on handler ' + self.handler)
        self.client.subscribe(subscribe_path)

    def on_message(self, client, userdata, msg):
        self.logger.log('Message on topic ' + msg.topic + (str('\n'+msg.payload) if self.log_with_payload else ''))

        # iterate over all tasks configured in the
        # config and use the api to send it
        for taskModule, taskClass in config.apitasks:
            the_task = getattr(importlib.import_module(taskModule), taskClass)
            the_task = the_task()
            the_task.send(msg)
            the_task.close()
            del the_task

        # db tasks
        for taskModule, taskClass in config.dbtasks:
            the_task = getattr(importlib.import_module(taskModule), taskClass)
            the_task = the_task()
            the_task.save(self.app['id'], msg)
            the_task.close()
            del the_task # not sure yet if this makes sense or is GC'ed anyway

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.logger.log('Unexcepted disconnect from app ' + str(userdata) + '. Reason: ' + str(rc), 'RECONNECT')
            random.seed()
            sleep_duration = random.randint(self.min_sleep_time, self.max_sleep_time)
            self.logger.log('Sleeping for ' + str(sleep_duration) + 's...', 'RECONNECT')
            sleep(sleep_duration)

            self.app = self.db.get_application(self.id)
            if self.app:
                self.logger.log('Sleep finished. Got new app credentials. Retrying connection...', 'RECONNECT')
                self.client.username_pw_set(self.app['app_id'], self.app['app_key'])
                self.client.connect_async(self.handler, 1883, 60)

    def set_interval(self, func, sec):
        def func_wrapper():
            self.set_interval(func, sec)
            func()

        t = threading.Timer(sec, func_wrapper)
        t.start()
        return t
