import numpy as np


class DeviceMemory:
    def __init__(self, shape):
        self.max_memory_cnt = shape[0]
        # self.memory_len = shape[1]
        self.memory_cnt = 0
        self.array = np.zeros(shape, dtype=np.float16)

    def store(self, data):
        # out of bound
        if self.memory_cnt >= self.max_memory_cnt:
            return
        # store
        self.array[self.memory_cnt, :] = np.array(data, dtype=np.float16)
        self.memory_cnt += 1


class DeviceDatabass:
    def __init__(self, history_shape: tuple):
        self.device_cnt = 0
        self.shape = history_shape
        self.dbs = {}

    def add(self, id):
        self.dbs[id] = DeviceMemory(self.shape)
        self.device_cnt += 1

    def get(self, id) -> DeviceMemory:
        return self.dbs.get(id)

    def store(self, id, data):
        db = self.get(id)
        db.store(data)

    def check_id(self, id):
        return id in self.dbs.keys()
