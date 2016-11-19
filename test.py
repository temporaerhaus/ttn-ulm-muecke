# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print('connected')
    print('subscribing to +/devices/+/up')
    client.subscribe('+/devices/+/up')


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def on_subscribe(client, userdata, mid, granted_qos):
    print('subscribed')


print('starting...')
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

client.username_pw_set('70B3D57ED000146F', 'f6uPW0DYDdHCaPJgTByo0IwqWLcVK2EpAsdEKfAnl6c=')
client.connect('staging.thethingsnetwork.org', 1883, 60)

client.loop_forever()
