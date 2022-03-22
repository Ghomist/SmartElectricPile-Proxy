import json


def _init():
    global config
    config = {}
    # Init config
    with open('DEVICES-KEY.bib') as f:
        config.update(json.loads(f.read()))
    with open('config.json') as f:
        config.update(json.loads(f.read()))
        # Update device id into config
        for k, topic in config['cloud']['topics'].items():
            config['cloud']['topics'][k] = topic.format(config['device_id'])


_init()
