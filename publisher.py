# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
import json
import base64

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

dev_eui = 'client1'
app_id = 'flrp-mqtt'
access_key = 'ttn-account-v2.yhZqDItky9xTY8DPgqKJpcSWVtHfIeTs9Fy6txl_8Hg'

client = mqtt.Client()
client.on_connect = on_connect

client.username_pw_set(app_id, access_key)
client.connect('eu.thethings.network', 1883, 60)

client.loop_start()

while True:
    time.sleep(5)
    #msg = literal_eval('b"hallo welt"')
    #payload = json.dumps(dict(payload=base64.b64encode(msg).decode(), port=1, ttl='1h'))
    payload = json.dumps(dict(msg='flurp labs'))
    channel = app_id + '/devices/' + dev_eui + '/down'
    print(channel, payload)
    client.publish(channel, payload)
