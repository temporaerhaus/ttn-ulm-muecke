# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
import json
from ast import literal_eval
import base64


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

dev_eui = '0000000081F88297'
app_eui = '70B3D57ED0001627'
access_key = '7gf+WnmpNHipjcVEcVLJXNn31SxYJOpgrFhKPVJs8OM='

client = mqtt.Client()
client.on_connect = on_connect

client.username_pw_set(app_eui, access_key)
client.connect('staging.thethingsnetwork.org', 1883, 60)

client.loop_start()

while True:
    time.sleep(5)
    msg = literal_eval('b"2508"')
    payload = json.dumps(dict(payload=base64.b64encode(msg).decode(), port=1, ttl='1h'))
    print(payload)
    client.publish(app_eui+'/devices/'+dev_eui+'/down', payload)
