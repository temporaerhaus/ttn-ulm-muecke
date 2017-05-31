# Dustfetcher
A server that subscribes to many MQTT streams (or applications) on the TTN network 
and saves the sensor data into a MySQL database.

Supports hot reloading. When an app was added or removed from the database, the service
will subscribe or unsubscribe from this MQTT stream.

## Dependencies
* paho-mqtt
* PyMySQL
* influxdb
* requests

It's only tested with Python 3. Could work on Python 2, but I don't know :)

## Install
* Run the create table commands in schema/database.sql
* Edit the config and insert your database credentials

## Usage
The best is to use a virtual_env to handle all the dependencies. But besides that, just run

```
python3 server.py
```

...or create a systemd service for a more stable service.


## License
AGPL 3.0

See agpl-3.0.txt.