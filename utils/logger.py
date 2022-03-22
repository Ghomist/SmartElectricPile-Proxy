import json
import time


def _init():
    global max_len
    global cut_pos
    global time_log
    with open('utils/utils_config.json') as f:
        cfg = json.loads(f.read())
        max_len = cfg['logger']['max-len']
        cut_pos = int((max_len-4)/2)
        time_log = cfg['logger']['time-log']


def log(prefix, content):
    log = "["+prefix
    if time_log:
        log += " " + time.strftime('%H:%M:%S', time.localtime())
    log += "] "
    if len(content) < max_len:
        log += content
    else:
        log += content[:cut_pos-1]+'....'+content[1-cut_pos:]
    print(log)


_init()


if __name__ == "__main__":
    log('test', 'ccccttttentdddd!')
