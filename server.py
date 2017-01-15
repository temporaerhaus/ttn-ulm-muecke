# -*- coding: utf-8 -*-
import signal
import sys
import subscriber
import database
import paho.mqtt.client as mqtt
import threading

database = database.Database()
applications = database.get_applications()

# TODO: reload subscriber every 30s?

for app in applications:
    print('Handling app ' + app['app_id'])
    client = mqtt.Client()
    sub = subscriber.Subscriber(database, app, client)
    client.loop_start()


def signal_handler(signal, frame):
    #print('You pressed Ctrl+C!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to quit')
signal.pause()

while True:
    dummy_event = threading.Event()
    dummy_event.wait()




