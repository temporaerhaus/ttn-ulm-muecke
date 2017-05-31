# -*- coding: utf-8 -*-
database = dict(
    host='localhost',
    database='muecke',
    user='muecke',
    password='muecke'
)

main = dict(
    save_to_db=True,
    send_to_api=True,
    api_endpoint='http://api.luftdaten.info/v1/push-sensor-data/'
)

# active api tasks
apitasks = [
    #('tasks.luftdaten', 'LuftdatenTask')
]

# active db tasks
dbtasks = [
    ('tasks.dbtask', 'DBTask'),
    #('tasks.influx', 'InfluxDBTask'),
]
