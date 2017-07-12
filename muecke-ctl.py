#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import database

parser = argparse.ArgumentParser(description='Add or delete an app')

parser.add_argument('action', choices=['add', 'delete', 'list'])
parser.add_argument('--appid', '-a', dest='appid')
parser.add_argument('--key', '-k', dest='key')
parser.add_argument('--handler', '-u', dest='handler')

args = parser.parse_args()

db = database.Database()
if args.action == 'add':
    db.add_application(args.appid, args.key, args.handler)
    print("Added")
elif args.action == 'delete':
    db.delete_application(args.appid, args.key)
    print("Deleted")
elif args.action == 'list':
    apps = db.get_applications()
    for app in apps:
        print("App: {0:24} Handler: {1}".format(app['app_id'], app['handler']))

