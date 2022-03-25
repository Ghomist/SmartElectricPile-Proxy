import paho.mqtt.client as mqtt

import raspberrypie.events as events


def init():
    # Client id, protocol version
    global client
    client = mqtt.Client(client_id="", protocol=mqtt.MQTTv311)

    # Client id, username
    # client.username_pw_set(username, password)

    # Callbacks
    client.on_connect = events.on_connect
    client.on_message = events.on_message
    client.message_callback_add("dev/+/up/data", events.upload)


def get_local_client():
    return client
