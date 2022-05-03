from socket import *
import threading


class SocketServer(threading.Thread):
    def __init__(self, port: int):
        threading.Thread.__init__(self)
        self.conn_dict = {}
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(('127.0.0.1', port))
        self.server.listen(1)
        self.cnt = 0

    def run(self):
        while True:
            conn, addr = self.server.accept()
            # Set keep alive
            conn.setsockopt(SOL_SOCKET, SO_KEEPALIVE, True)
            # conn.ioctl(SIO_KEEPALIVE_VALS, (
            #     1,          # Keep alive: on
            #     60*1000,    # Start to test alive: 1 min
            #     30*1000     # Interval: 60s
            # ))
            # Archive
            id = conn.recv(4)
            self.conn_dict[str(id)] = conn
            # Thread to listen
            threading.Thread(target=self.listen_to, args=[conn]).start()
            print(f'Receive: {id}')

    def listen_to(self, conn: socket):
        while True:
            data = conn.recv(10).decode('utf-8')
            if not data:
                conn.close()
                break
            # Step to do
            self.cnt += 1
            print(f'[{self.cnt}] {data}')

    def send_to(self, id: int, msg: str):
        id = str(id)
        target_soc: socket = self.conn_dict[id]
        target_soc.send(msg)
