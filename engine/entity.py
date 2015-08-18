# -*- coding: utf-8 -*-

"""
engine.entity
~~~~~~~~
A simple entity system

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

import uuid
import pymunk


class EntityManager(pymunk.Space):
    """
    Lord of all entities

    #TODO: document this as well
    """
    def __init__(self):
        """Constructor"""
        super().__init__()
        self._ents = {}
        self._classes = {}
        self._msg_queue = []

    def register_class(self, class_id, cls):
        """Register an Entity class"""
        self._classes[class_id] = cls

    def create_entity(self, class_id, **kwargs):
        """Create new entity instance

        Args:
            class_id(str): class id
        Returns:
            The new created entity
        """
        # uuid for this new entity
        new_uuid = uuid.uuid4().hex

        # create the actual entity
        entity = self._classes[class_id](new_uuid, manager=self, **kwargs)

        # TODO: document this!
        self.add(entity, entity.box)

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


class Entity(pymunk.Body):
    """
    Entity unit

    A general purpose object which is meant to be put
    into game scene. This object only holds an UUID,
    a boundary box and a series of arbitrary attributes
    (e.g. "cg_color", "glow", etc.).

    An entity implements a pymunk.Body, so all physics
    are applied to the out-of-the-box.

    An entity is not meant to be used as a unit performing logic
    on its behalf but rather a simple object holding information
    to be used by its manager.

    """
    def __init__(self, uuid, *, manager,
                 mass=100, position=(0, 0), size=(32, 32), **kwargs):
        """Constructor

        Args:
            uuid(str): uuid assigned to this entity
        Kwargs:
            position(tuple): Initial position
            size(tuple): Boundary box size for this entity
            manager(EntityManager): this entity's manager
        """

        # Assign manager and UUID for this entity
        self._manager = manager
        self._uuid = uuid

        # size
        self._width, self._height = size

        # Set moment (inertia) for this body
        moment = pymunk.moment_for_box(mass, self._width, self._height)

        # Call my parent
        super().__init__(mass, moment)

        # boundary box for this body
        self._box = pymunk.Poly.create_box(self, size)

        # position
        self.position = position

        #
        # Contacts directory:
        # In order for entity to be able to communicate with other entities,
        # it will need to posses a directory from which each of its peers
        # can be referred to by a friendly name instead of its raw UUID, very
        # much like having a contact list on your smartphone. With this
        # approach, any entity can easily send messages to another one
        self._directory = {}

    @property
    def manager(self):
        return self._manager

    @property
    def box(self):
        """Rectangle"""
        return self._box

    @property
    def width(self):
        """Boundary box width"""
        return self._width

    @property
    def height(self):
        """Boundary box height"""
        return self._height

    @property
    def uuid(self):
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
