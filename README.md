# Muecke
A server that subscribes to many MQTT streams (or applications) on the TTN network 
and saves the (sensor) data into a MySQL or InfluxDB database. If enabled, it can
redirect the sensor data to another HTTP API, example included.

Supports hot reloading. When an app was added or removed from the database, the service
will subscribe to or unsubscribe from this MQTT stream.

## Main dependencies
* paho-mqtt
* PyMySQL
* influxdb
* requests

It's only tested with Python 3. Could work on Python 2, but I don't know :)

## Install
* Install MySQL/MariaDB and/or InfluxDB, according to the docs of these services.
* For MySQL: Run the 'CREATE TABLE' commands in schema/database.sql
* For InfluxDB: Just install and create a database. Credentials and database name can be set in config.py.
* Edit the config and insert your database credentials

## Usage
Create a virtual environment, enter it and install all dependencies:

```
virtualenv <custom-path-to-virtual-env>
source <custom-path-to-virtual-env>/bin/activate
```

Install all dependencies:

```
pip install -r requirements.txt
```

Run the server:

```
python3 server.py
```

...or create a systemd service for a more stable service.


## License
AGPL 3.0

See agpl-3.0.txt.