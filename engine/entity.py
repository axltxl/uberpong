# -*- coding: utf-8 -*-

import uuid

class EntityManager:
    def __init__(self):
        self._ents = {}
        self._classes = {}
        self._msg_queue = []

    def register_class(self, id, cls):
        self._classes[id] = cls

    def create_entity(self, id):
        uuid = uuid.uuid4().hex
        entity = self._classes[id](uuid, manager=self)
        self._ents[uuid] = entity
        return entity

    def dispatch_messages(self):
        while len(self._msg_queue):
            msg = self._msg_queue.pop()
            entity_dst = self._ents[msg['to']]
            entity_dst.on_message(msg)

    def queue_message(self, msg):
        self._msg_queue.append(msg)


class Entity:
    def __init__(self, uuid, *, manager):
        super.__init__(self)
        self._manager = manager
        self._uuid = uuid
        self._directory = {}

    def get_uuid(self):
        return self._uuid

    def send_message(self, *, to, data):
        self._manager.queue_message(
            {
                "from": self._uuid,
                "to": self._directory[to],
                "data": data
            }
        )

    def add_to_directory(self, name, uuid):
        self._directory[name] = uuid

    def on_message(self, msg):
        pass
