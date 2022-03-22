import paho.mqtt.client as mqtt
import json

import config
import huaweicloud.client as cloud

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
    print('[local] '+log)


def on_message(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    print('[local] '+message.payload)
    upload = {
        "services": [
            {
                "service_id": "Temperature",
                "properties": {
                    "value": "33"
                }
            },
            {
                "service_id": "UploadTest",
                "properties": {
                    "Text": "Hello HuaweiCloud",
                    "Integer": 2399
                }
            },
            {
                "service_id": "LightControl",
                "properties": {
                    "State": 3,
                }
            }
        ]
    }
    cloud.get_cloud_client().publish(
        f'$oc/devices/{config.get_cfg()["device_id"]}/sys/properties/report',
        payload=json.dumps(upload)
    )
