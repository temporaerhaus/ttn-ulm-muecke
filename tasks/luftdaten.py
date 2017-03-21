# -*- coding: utf-8 -*-
import json
import requests
from tasks.apitask import APITask
from logger import Logger


class LuftdatenTask(APITask):
    logger = None
    id_prefix = 'TTNUlm-'
    api_endpoint = 'https://api.luftdaten.info/v1/push-sensor-data/'
    api_madavi_endpoint = 'https://api-rrd.madavi.de/data.php'

    def __init__(self):
        self.logger = Logger()
        APITask.__init__(self)

    def send(self, mqtt_msg):
        self.logger.log('Executing API task...')
        json_raw = mqtt_msg.payload.decode("utf-8")
        data = json.loads(json_raw)

        device_eui = int(data['hardware_serial'], 16)

        if 'payload_fields' in data:
            payload_fields = data['payload_fields']
        else:
            payload_fields = None

        if not all(k in payload_fields for k in ('pm10', 'pm25', 'temperature', 'humidity')):
            self.logger.log('Not a particulates message.')
            return

        # ***************************
        # Feinstaub sensor (SDS011)
        # ***************************
        # X-Pin: 1 für SDS011, 3 für BMP180, 5 für PPD42NS, 7 für DHT22 und 11 für BME280.
        headers = {
            'X-Pin': '1',  # SDS011 == 1
            'X-Sensor': self.id_prefix + str(device_eui)
        }
        postdata = {
            'software_version': 'TTNUlm-v1',
            'sensordatavalues': [
                {'value_type': 'P1', 'value': str(payload_fields['pm10'])},  # PM10
                {'value_type': 'P2', 'value': str(payload_fields['pm25'])}   # PM2.5
            ]
        }
        try:
            r = requests.post(self.api_endpoint, json=postdata, headers=headers)
            r = requests.post(self.api_madavi_endpoint, json=postdata, headers=headers)
        except requests.ConnectionError as e:
            self.logger.log('Connection error: ' + e.message, tag='ERROR')
            self.logger.log('({0}): {1}'.format(e.errno, e.strerror, tag='ERROR'))

        # ***************************
        # Temp/Hum (DHT)
        # ***************************
        headers = {
            'X-Pin': '7',  # DHT22 == 7
            'X-Sensor': self.id_prefix + str(device_eui)
        }
        postdata = {
            'software_version': 'TTNUlm-v1',
            'sensordatavalues': [
                {'value_type': 'temperature', 'value': str(payload_fields['temperature'])},
                {'value_type': 'humidity', 'value': str(payload_fields['humidity'])},
            ]
        }
        try:
            r = requests.post(self.api_endpoint, json=postdata, headers=headers)
            r = requests.post(self.api_madavi_endpoint, json=postdata, headers=headers)
        except requests.ConnectionError as e:
            self.logger.log('Connection error: ' + e.message, tag='ERROR')
            self.logger.log('({0}): {1}'.format(e.errno, e.strerror, tag='ERROR'))
