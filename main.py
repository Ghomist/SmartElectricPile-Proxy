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
    cloud_client.connect(cfg['cloud']['url'], port=cfg['cloud']['port'])
    cloud_client.subscribe(
        (f"$oc/devices/{cfg['device_id']}/sys/messages/down", 0)
    )

    # raspberry pie
    pie.init()
    local_client = pie.get_local_client()
    local_client.connect(cfg['local']['url'], port=cfg['local']['port'])
    local_client.subscribe(
        ("$dev/+/up/data", 0)
    )

    # Start
    Thread(None, cloud_client.loop_forever).start()
    Thread(None, local_client.loop_forever).start()
    # print("Connecting finished.")


if __name__ == "__main__":
    main()
