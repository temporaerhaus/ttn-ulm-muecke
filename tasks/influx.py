# -*- coding: utf-8 -*-
import json
from tasks.dbtask import DBTask
from logger import Logger
from influxdb import InfluxDBClient


class InfluxDBTask(DBTask):
    logger = None

    def __init__(self):
        self.logger = Logger()
        DBTask.__init__(self)

    def save(self, app_id, mqtt_msg):
        self.logger.log('Executing Influx task...', 'TASK-INFLUX')
        json_raw = mqtt_msg.payload.decode("utf-8")
        data = json.loads(json_raw)

        influx_json = [{
            "measurement": "cpu_load_short",
            "tags": {
                "host": "",
            },
            "time": "2009-11-10T23:00:00Z",
            "fields": {
                "value": 0.64
            }
        }
        ]

        device_eui = int(data['hardware_serial'], 16)

        #client = InfluxDBClient('localhost', 8086, 'muecke', 'muecke', 'muecke')
        #self.logger.log('Saving JSON payload to InfluxDB.')
        #client.write_points(json_raw)

        #result = client.query('select value from cpu_load_short;')
        #print("Result: {0}".format(result))

    def close(self):
        # TODO close influx connection?
        pass
