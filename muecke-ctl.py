#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import database

# command line tool for adding/changing/deleting apps
# TODO: add app, delete app, change access key, list all apps

parser = argparse.ArgumentParser(description='Add or delete an app')

parser.add_argument('action', choices=['add', 'delete'])
parser.add_argument('--app-id', '-a', dest='appid', required=True)
parser.add_argument('--key', '-k', dest='key', required=True)
parser.add_argument('--handler', '-u', dest='handler')

args = parser.parse_args()

db = database.Database()
if args.action == 'add':
    db.add_application(args.appid, args.key, args.handler)
    print("Added")
elif args.action == 'delete':
    db.delete_application(args.appid, args.key)
    print("Deleted")

