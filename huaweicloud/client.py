import paho.mqtt.client as mqtt
from threading import Thread

import huaweicloud.client_id_generator as generator
from config import *


class CloudClient:
    def __init__(self, device_id, secret, log_all=False):
        self.log = log_all
        # Client id, username, password
        self.client_id, self.username, self.password = generator.generate(device_id, secret)

        # Client id, protocol version
        self.client = mqtt.Client(client_id=self.client_id, protocol=mqtt.MQTTv311)

        # Client id, username
        self.client.username_pw_set(self.username, self.password)

        # Set callback functions
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.message_callback_add(cloud_topics['all'], self.on_message)
        self.client.message_callback_add(cloud_topics['cmd'], self.on_command_down)

        # subscribe
        self.client.subscribe()

    def start(self):
        Thread(target=self.client.loop_forever).start()

    def stop(self):
        # self.client.loop_stop()
        self.client.disconnect()

    def on_connect(self, client: mqtt.Client, userdata, flags, rc):
        log = f'Connect with return code: {str(rc)} ({on_rc(rc)})'
        logger.log('cloud', log)

    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        if self.log:
            payload = msg.payload.decode('utf-8')
            logger.log('cloud', payload)

    def on_disconnect(self, client, userdata, rc):
        logger.log('cloud', f"Disconnet(rc: {str(rc)})")

    def on_command_down(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        # TODO
        return

        # Exclude respone messages
        if "response" in msg.topic:
            return

        payload = json.loads(msg.payload)
        # Down command
        if payload['service_id'] == "SwitchLight":
            cmd = {
                "cmd": payload['command_name']
            }
            local.get_local_client().publish(
                config['local']['topics']['down'],
                payload=json.dumps(cmd),
                qos=1
            )

        respone_cmd(msg.topic)
