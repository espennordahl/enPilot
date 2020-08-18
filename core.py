import logging

logger = logging.getLogger(__name__)

class Base:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        logger.error("Name is read-only")
        raise Exception

    def serialize(self):
        root = {}
        root["name"] = self.name

        return root

class Asset(Base):
    pass

class Shot(Base):
    pass

