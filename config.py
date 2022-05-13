import json

# DO NOT MODIFY
with open('DEVICES-KEY.bib') as bib:
    _devices_key = json.load(bib)
    device_id = _devices_key['device_id']
    secret = _devices_key['secret']

# cloud settings
cloud_url = 'a16236a40f.iot-mqtts.cn-north-4.myhuaweicloud.com'
cloud_port = 1883
cloud_topics = {
    "all": "$oc/#",
    "report": f"$oc/devices/{device_id}/sys/properties/report",
    "cmd": f"$oc/devices/{device_id}/sys/commands/#",
    # "msg-down": f"$oc/devices/{device_id}/sys/messages/down"
}

# local client settings
local_url = '127.0.0.1'
local_port = 1883
local_topics = {
    "all": "dev/#",
    "login": "dev/+/login",
    "data": "dev/+/data",
    "report": "dev/+/report",
    "cmd": "dev/+/cmd"
}


def specific_cmd(id=None):
    """
    Get specific topic for each device with their id
    NONE FOR ALL
    """
    if id:
        return local_topics['cmd'].replace('+', id)
    else:
        return local_topics['cmd']


def respone_cmd(topic):
    """Respone code\nDefault: true"""
    return "commands/response/".join(topic.split('commands/'))
