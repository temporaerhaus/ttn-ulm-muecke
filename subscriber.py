# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import database
import json
import base64
from threading import Thread


class Subscriber:
    client = None
    database = None

    applications = [
        ['70B3D57ED000146F', 'f6uPW0DYDdHCaPJgTByo0IwqWLcVK2EpAsdEKfAnl6c='],
        ['70B3D57ED0001627', '7gf+WnmpNHipjcVEcVLJXNn31SxYJOpgrFhKPVJs8OM='],
        ['70B3D57ED0001628', 'zRaOnksfOH+i/XyoSMz70+QZ0rn7xbyLlYfs+xB8DIg=']
    ]

    def __init__(self):
        self.database = database.Database()

    def worker(self, app, count):
        c = str(count)
        print('[thread'+c+'] thread started\n')
        print('[thread'+c+'] connection to '+app[0]+' '+app[1]+'\n')

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.username_pw_set(app[0], app[1])
        self.client.connect_async('staging.thethingsnetwork.org', 1883, 60)
        self.client.loop_forever()

    def start(self):
        print('starting...')
        c = 1
        for app in self.applications:
            t = Thread(target=self.worker, args=(app, c))
            t.start()
            c += 1

    def on_connect(self, client, userdata, flags, rc):
        print('connected')
        subscribe_path = '+/devices/+/up'
        print('subscribing to ' + subscribe_path)
        self.client.subscribe(subscribe_path)

    def on_message(self, client, userdata, msg):
        print('got message')
        print(msg.topic + " " + str(msg.payload))

        payload_as_json = json.loads(msg.payload)
        payload_decoded = base64.b64decode(payload_as_json['payload'])

        self.database.save(payload_as_json['dev_eui'], payload_decoded, str(msg.payload))
