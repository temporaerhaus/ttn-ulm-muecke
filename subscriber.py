# -*- coding: utf-8 -*-

class Subscriber:
    client = None
    database = None
    app = None

    def __init__(self, database, app, client):
        self.database = database
        self.app = app
        self.client = client

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.username_pw_set(self.app['app_id'], self.app['app_key'])
        self.client.connect_async('eu.thethings.network', 1883, 60)

    def on_connect(self, client, userdata, flags, rc):
        print('connected')
        subscribe_path = '+/devices/+/up'
        print('subscribing to ' + subscribe_path)
        self.client.subscribe(subscribe_path)

    def on_message(self, client, userdata, msg):
        print('got message')
        print(msg.topic + " " + str(msg.payload))
        self.database.save(self.app['id'], msg)
