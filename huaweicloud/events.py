import paho.mqtt.client as mqtt
import json

import config
import raspberrypie.client as local

on_rc = {
    '0': "Accepted",
    '1': "Refused, unacceptable protocol version",
    '2': "Refused, identifier rejected",
    '3': "Refused, server unavailable",
    '4': "Refused, bad user name or password",
    '5': "Refused, not authorized",
}


def on_connect(client: mqtt.Client, userdata, flags, rc):
    log = 'Connect with return code: {} ({})'.format(
        str(rc),
        on_rc.get(str(rc), "Unknown return code")
    )
    print('[cloud] '+log)


def on_message(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    print(f'[cloud] Topic: {message.topic}')
    if mqtt.topic_matches_sub("$oc/#", message.topic):
        msg = json.loads(message.payload)
        # Log
        print('[cloud] Msg: '+str(msg))
        # Down command
        if msg['service_id'] == "ReceiveTest" and msg['command_name'] == "DownInt":
            local.get_local_client().publish(
                "dev/01/down/cmd",
                payload=msg['paras']['Number'],
                qos=0
            )
