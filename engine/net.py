# -*- coding: utf-8 -*-

import socket
import json

class Channel:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def pump(self):
        data, addr = self.sock.recvfrom(1024)
        data_str = data.decode("utf-8")
        try:
            data_obj = json.loads(data_str)
        except ValueError:
            data_obj = {}
        self.on_data_received(data_obj, addr[0], addr[1])

    def send(self, data, host, port):
        self.sock.sendto(bytes(json.dumps(data), "utf-8"), (host, port))

    def on_data_received(self, data, host, port):
        pass

class Client(Channel):
    def __init__(self, *, host='localhost', port):
        self._server_host = host
        self._server_port = port

    def send(self, data):
        super().send(data, self._server_host, self._server_port)

class Server(Channel):
    def __init__(self, *, port):
        super().__init__()
        self.sock.bind(("", port))

    def on_data_received(self, data, host, port):
        self.send({"hello":"world"}, host, port)

def test():
    server = Server(port=5000)
    #client = Client(port=5000)
    while True:
        server.pump()
        #client.pump()

if __name__=='__main__':
    test()
