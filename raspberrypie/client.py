import paho.mqtt.client as mqtt

import raspberrypie.events as events
from config import config


def init():
    # Client id, protocol version
    global client
    client = mqtt.Client(client_id="mqtt_proxy", protocol=mqtt.MQTTv311)

    # Client id, username
    # client.username_pw_set(username, password)

    # Callbacks
    client.on_connect = events.on_connect
    client.on_disconnect = events.on_disconnect
    client.message_callback_add(config['local']['topics']['all'], events.on_message)
    client.message_callback_add(config['local']['topics']['up'], events.upload)


def get_local_client():
    return client
