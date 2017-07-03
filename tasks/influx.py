# -*- coding: utf-8 -*-
import json
from tasks.dbtask import DBTask
from logger import Logger
from influxdb import InfluxDBClient
import config


class InfluxDBTask(DBTask):
    logger = None

    def __init__(self):
        self.logger = Logger()
        DBTask.__init__(self)

    def save(self, app_id, mqtt_msg):
        self.logger.log('Executing Influx task...', 'TASK-INFLUX')

        json_raw = mqtt_msg.payload.decode("utf-8")
        data = json.loads(json_raw)

        topic_splitted = mqtt_msg.topic.split('/')
        dev_eui = topic_splitted[2]

        best_rssi = -1000
        best_gateway = ''
        best_snr = -1000
        best_received = ''
        if 'gateways' in data['metadata']:
            for gateway in data['metadata']['gateways']:
                if gateway['rssi'] > best_rssi:
                    best_rssi = gateway['rssi']
                    best_gateway = gateway['gtw_id']
                    best_snr = gateway.get('snr', 0)
                    best_received = gateway['time']

        self.logger.log('best_rssi: %d' % best_rssi)
        self.logger.log('best_gateway: %s' % best_gateway)
        self.logger.log('best_snr: %d' % best_snr)
        self.logger.log('best_received: %s' % best_received)

        if 'payload_fields' in data:
            payload_fields = json.dumps(data['payload_fields'])
        else:
            payload_fields = None

        influx_json = [{
            'measurement': 'ttndata',
            'tags': {
                'dev_eui': str(dev_eui),
                'app_id': int(app_id),
            },
            'time': best_received,
            'fields': {
                'best_rssi': float(best_rssi),
                'best_gateway': str(best_gateway),
                'best_snr': float(best_snr),
                'best_received': str(best_received),

                'payload_fields': str(payload_fields),
                'payload_raw': str(data['payload_raw']),

                'gateways': json.dumps(data['metadata']['gateways']) if 'gateways' in data['metadata'] else ''
            }
        }]

        # add all custom fields
        if 'payload_fields' in data:
            self.logger.log(str(data['payload_fields']), 'INFO')
            for key, value in data['payload_fields'].items():
                influx_json[0]['fields'][key] = value

        client = InfluxDBClient(
            config.influxdb['host'],
            config.influxdb['port'],
            config.influxdb['user'],
            config.influxdb['password'],
            config.influxdb['database']
        )
        self.logger.log('Saving JSON payload to InfluxDB.')
        client.write_points(influx_json)

    def close(self):
        # TODO close influx connection?
        pass
