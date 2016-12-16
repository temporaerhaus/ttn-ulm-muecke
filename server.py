# -*- coding: utf-8 -*-
import subscriber
import database
import paho.mqtt.client as mqtt
import threading

database = database.Database()
applications = database.get_applications()

for app in applications:
    print('Handling app ' + app['app_id'])
    client = mqtt.Client()
    sub = subscriber.Subscriber(database, app, client)
    client.loop_start()

while True:
    dummy_event = threading.Event()
    dummy_event.wait()
