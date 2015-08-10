# -*- coding: utf-8 -*-

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
        uuid = uuid.uuid4().hex

        # create the actual entity
        entity = self._classes[id](uuid, manager=self, **kwargs)

        # map the entity
        self._ents[uuid] = entity

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
    def __init__(self, uuid, *, manager):
        """Constructor

        Args:
            uuid(str): uuid assigned to this entity
        Kwargs:
            manager(EntityManager): this entity's manager
        """

        self._manager = manager
        self._uuid = uuid

        #
        # Contacts directory:
        # In order for entity to be able to communicate with other entities,
        # it will need to posses a directory from which each of its peers
        # can be referred to by a friendly name instead of its raw UUID, very
        # much like having a contact list on your smartphone. With this
        # approach, any entity can easily send messages to another one
        self._directory = {}

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
