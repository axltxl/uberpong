# -*- coding: utf-8 -*-

"""
engine.entity
~~~~~~~~
A simple entity system

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

import uuid


class EntityManager:
    """Lord of all entities"""
    def __init__(self):
        """Constructor"""
        self._ents = {}
        self._classes = {}
        self._msg_queue = []

    def register_class(self, id, cls):
        """Register an Entity class"""
        self._classes[id] = cls

    def create_entity(self, id, **kwargs):
        """Create new entity instance

        Args:
            id(str): class id
        Returns:
            The new created entity
        """
        # uuid for this new entity
        new_uuid = uuid.uuid4().hex

        # create the actual entity
        entity = self._classes[id](new_uuid, manager=self, **kwargs)

        # map the entity
        self._ents[new_uuid] = entity

        # give the new entity back
        return entity

    def dispatch_messages(self):
        """Deliver all pending messages"""
        while len(self._msg_queue):
            msg = self._msg_queue.pop()
            entity_dst = self._ents[msg['to']]
            entity_dst.on_message(msg)

    def queue_message(self, msg):
        """Queue a new message"""
        self._msg_queue.append(msg)


class Entity:
    def __init__(self, uuid, *, manager,
                 position=(0, 0), size=(32, 32), anchor=(0, 0)):
        """Constructor

        Args:
            uuid(str): uuid assigned to this entity
        Kwargs:
            manager(EntityManager): this entity's manager
        """

        self._manager = manager
        self._uuid = uuid

        # size
        self._width, self._height = size

        # Position + boundary box
        self._update_box(position)

        #
        # Contacts directory:
        # In order for entity to be able to communicate with other entities,
        # it will need to posses a directory from which each of its peers
        # can be referred to by a friendly name instead of its raw UUID, very
        # much like having a contact list on your smartphone. With this
        # approach, any entity can easily send messages to another one
        self._directory = {}

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self._update_box()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self._update_box()

    def _update_box(self, position=None):
        if position is not None:
            self._a, self._b = position
        self._c = self._a + self._width
        self._d = self._b + self._height

    def move_abs(self, x=0, y=0):
        self._update_box((x, y))

    def move_rel(self, dx=0, dy=0):
        self._update_box((self._a + dx, self._b + dy))

    def get_uuid(self):
        """Get UUID of this entity"""
        return self._uuid

    def send_message(self, *, to, data):
        """Send a message to another entity

        Kwargs:
            to(str): friendly name of the destination entity
            data(dict): variable data to be sent to the destination entity
        """
        self._manager.queue_message(
            {
                "from": self._uuid,  # Remitent UUID (this entity's UUID)
                "to": self._directory[to],  # Destination entity's UUID
                "data": data  # Arbitrary data to be sent to this entity
            }
        )

    def add_to_directory(self, name, uuid):
        """Add an entity to this entity's directory

        Args:
            name: Friendly name to be associated to the UUID
            uuid: Unique identifier of the entity to be added to the directory
        """
        self._directory[name] = uuid

    def on_message(self, msg):
        """This will be invoked anytime this entity receives a message

        Args:
            msg(dict): Message envelope containing all relevant data
        """
        pass
