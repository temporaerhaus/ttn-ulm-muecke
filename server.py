# -*- coding: utf-8 -*-
import signal
import sys
import subscriber
import database
import paho.mqtt.client as mqtt
import threading
import random
import string
from logger import Logger


class Server:
    db = None
    logger = None
    current_apps = []
    mqtt_clients = {}
    new_apps = []

    reload_interval = 20.0

    def __init__(self):
        self.db = database.Database()
        self.logger = Logger()

        for app in self.db.get_applications():
            self.current_apps.append(app['id'])

        # Subscribe
        self.subscribe_to_apps(self.current_apps)

        # Set timer
        self.reload()

        # SIGINT
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.pause()

    def subscribe_to_apps(self, apps):
        # code for the first run of then server to fetch and subscribe to all current apps
        for app_id in apps:
            app_to_subscribe = self.db.get_application(app_id)
            if app_to_subscribe:
                # looks like we get random disconnects from other instances if this id  is not unique
                random_chars = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
                client = mqtt.Client(client_id='client'+str(app_id)+random_chars,
                                     clean_session=False,
                                     userdata=app_to_subscribe['app_id'])
                sub = subscriber.Subscriber(app_to_subscribe, client)
                client.loop_start()
                self.mqtt_clients[app_id] = client

    def reload(self):
        self.logger.log('Timer fired, checking new and old apps...', 'TIMER')
        threading.Timer(self.reload_interval, self.reload).start()

        # get all current apps in db
        apps_in_database = []
        for app in self.db.get_applications():
            apps_in_database.append(app['id'])

        # compare with previous list. will contain all apps who are in both lists (schnittmenge)
        new_and_current_apps = set(self.current_apps).intersection(apps_in_database)
        new_apps = set(apps_in_database).difference(self.current_apps)

        # will contain all apps that where active but are deleted.
        # -> difference between new_and_current_apps and current_apps
        deleted_apps = set(self.current_apps).difference(new_and_current_apps)

        # check for new access keys (dirty bit)
        # TODO

        # start new subscribe, delete missing subscribes

        # 1) unsubscribe from deleted apps
        if len(deleted_apps):
            self.logger.log('Old apps to unsubscribe found', 'TIMER')
            for app_id in deleted_apps:
                self.logger.log('Unsubscribing from ' + str(app_id) + ' because this app was deleted', 'TIMER')
                self.mqtt_clients[app_id].unsubscribe('+/devices/+/up')
                self.mqtt_clients.pop(app_id, None)
        else:
            self.logger.log('No apps deleted since last interval', 'TIMER')

        # 2) subscribe to all new apps
        if len(new_apps):
            self.logger.log('New apps found. Subscribing...', 'TIMER')
            self.subscribe_to_apps(new_apps)
        else:
            self.logger.log('No new apps found. Sleeping...', 'TIMER')

        # Set all new and current apps as the new current apps, until the next interval
        self.current_apps = new_and_current_apps

    def signal_handler(self, signal, frame):
        sys.exit(0)

if __name__ == "__main__":
    server = Server()
