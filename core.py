import logging
import os

logger = logging.getLogger(__name__)

class Base:
    def __init__(self, name):
        self._name = name
        self.project = None

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

    @property
    def path(self):
        raise NotImplementedError

    @path.setter
    def path(self, path):
        logger.error("Path is read-only")
        raise Exception

class Asset(Base):
    pass
    @property
    def path(self):
        if not self.project:
            return None
        return os.path.join(self.project.path, "assets", self.name)

    def createOnDisk(self):
        rootpath = os.path.join(self.project.assetsDir, self.name)
        if not os.path.exists(rootpath):
            os.mkdir(rootpath)
        for folder in ["maya", "houdini", "nuke", "sandbox"]:
            swpath = os.path.join(rootpath, folder)
            if not os.path.exists(swpath):
                os.mkdir(swpath)



class Shot(Base):
    pass
    @property
    def path(self):
        if not self.project:
            return None
        return os.path.join(self.project.path, "shots", self.name)

    def createOnDisk(self):
        rootpath = os.path.join(self.project.shotsDir, self.name)
        if not os.path.exists(rootpath):
            os.mkdir(rootpath)
        for folder in ["maya", "houdini", "nuke", "sandbox"]:
            swpath = os.path.join(rootpath, folder)
            if not os.path.exists(swpath):
                os.mkdir(swpath)


