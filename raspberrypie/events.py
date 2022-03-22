import paho.mqtt.client as mqtt
import json

from config import config
import utils.logger as logger
import huaweicloud.client as cloud
from utils.mqtt_util import on_rc


def on_connect(client: mqtt.Client, userdata, flags, rc):
    log = f'Connect with return code: {str(rc)} ({on_rc(rc)})'
    logger.log('local', log)


def on_message(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    payload = message.payload.decode('utf-8')
    logger.log('local', payload)
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
        f'$oc/devices/{config["device_id"]}/sys/properties/report',
        payload=json.dumps(upload)
    )
