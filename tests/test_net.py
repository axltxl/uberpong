# -*- coding: utf-8 -*-

import uuid
from engine.net import Client, Server
from nose.tools import eq_, ok_, assert_raises, with_setup


class EchoClient(Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_received = {}

    def on_data_received(self, data, host, port):
        self.data_received = data


class EchoServer(Server):
    def on_data_received(self, data, host, port):
        self.send(data, host, port)


def get_uuid_pkt():
    return {"uuid_data": uuid.uuid4().hex}

data_sent = {}
server = EchoServer(port=5000)
client = EchoClient(port=5000)


def test_data_inconsistencies():
    # Try to send non-dict data
    assert_raises(TypeError, client.send, "")
    assert_raises(TypeError, client.send, 4)
    assert_raises(TypeError, client.send, True)

    # Capture data received before test
    data_received = client.data_received.copy()

    # Try to send empty data
    client.send({})

    # Pump events on both client and server
    server.pump()
    client.pump()

    # Empty data shouldn't update client.data_received
    eq_(data_received, client.data_received)

def test_continuity():
    for i in range(10):
        client.send({'number': i + 1})
        # Pump events on both client and server just ONCE
        server.pump()

    client.pump()

    # Expect client.data_received to have the last one
    eq_(client.data_received['number'], 10)


def test_data_eq():
    # Create data and send it to server
    data_sent = get_uuid_pkt()
    client.send(data_sent)

    # Pump events on both client and server
    server.pump()
    client.pump()

    # The actual test
    eq_(data_sent, client.data_received)
