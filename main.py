import paho.mqtt.client as mqtt
import json
from threading import Thread

import config
import huaweicloud.client as cloud
import raspberrypie.client as pie


def main():
    cfg = config.config

    # huawei cloud
    cloud.init(cfg['device_id'], cfg['secret'])
    cloud_client = cloud.get_cloud_client()
    try:
        cloud_client.connect(cfg['cloud']['url'], port=cfg['cloud']['port'])
        cloud_client.subscribe((cfg['cloud']['topics']['cmd-down'], 0))
    except ConnectionError:
        print("Failed connecting to cloud.")
        exit()

    # raspberry pie
    pie.init()
    local_client = pie.get_local_client()
    try:
        local_client.connect(cfg['local']['url'], port=cfg['local']['port'])
        local_client.subscribe((cfg['local']['topics']['up'], 0))
    except ConnectionRefusedError:
        print("No local broker found. Try with 'mosquitto'.")
        exit()

    # Start
    Thread(None, cloud_client.loop_forever).start()
    Thread(None, local_client.loop_forever).start()
    # print("Connecting finished.")
    # cloud_client.disconnect()
    # local_client.disconnect()


if __name__ == "__main__":
    main()
