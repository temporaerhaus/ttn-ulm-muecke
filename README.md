# Muecke
A server that subscribes to many MQTT streams (or applications) on the TTN network.

## Dependencies
* paho-mqtt
* PyMySQL

It's only tested with Python 3. Could work on Python 2, I don't know :)

## Install
* Run the create table commands in schema/database.sql
* Edit the config and insert your database credentials

## Usage
The best is to use a virtual_env to handle all the dependencies. But besided that, just run

```
python3 server.py
```
