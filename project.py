import logging
import os
import json
import datetime

from enPilot.core import Asset, Shot

logger = logging.getLogger(__name__)

class Project:
    def __init__(self, name):
        self._name = name
        self.shots = {}
        self.assets = {}
        if self._isProjectOnDisk():
            self._initFromDisk()

    def _initFromDisk(self):
        for asset in [x for x in os.listdir(self.assetsDir) if os.path.isdir(os.path.join(self.path, x))]:
            self.assets[asset] = Asset(asset)
        for shot in [x for x in os.listdir(self.shotsDir) if os.path.isdir(os.path.join(self.path, x))]:
            self.shots[shot] = Shot(shot)
        return

    @classmethod
    def projectsDir(cls):
        projectDir = os.getenv("PROJECTS_ROOT")
        if not projectDir:
            logger.error("PROJECTS_ROOT environment variable not found")
            raise Exception
        return projectDir


    @classmethod
    def listProjects(cls):
        projectDir = cls.projectsDir()
        projectList = [x for x in os.listdir(projectDir) if os.path.isdir(os.path.join(projectDir,x))]
        ## TODO: Check validity of project
        return projectList

    @classmethod
    def mainConfigFileName(cls):
        return "project.json"

    @property
    def assetsDir(self):
        return os.path.join(self.path, "assets")

    @property
    def shotsDir(self):
        return os.path.join(self.path, "shots")

    @property
    def configDir(self):
        return os.path.join(self.path, "config")

    @property
    def exists(self):
        return self._isProjectOnDisk()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        logger.error("Project name is read-only")
        raise Exception


    def addShot(self, shot):
        ## TODO: Check for string vs Shot object
        shot.project = self
        self.shots[shot.name] = shot

    def addAsset(self, asset):
        ## TODO: Check for string vs Asset object
        asset.project = self
        self.assets[asset.name] = asset

    def serialize(self):
        data = {"assets" : {},
                "shots": {}
                }

        data["name"] = self.name

        for asset in self.assets.values():
            data["assets"][asset.name] = asset.serialize()

        for shot in self.shots.values():
            data["shots"][shot.name] = shot.serialize()

        return data

    def _isProjectOnDisk(self):
        return self.name in Project.listProjects()

    @property
    def path(self):
        return os.path.join(Project.projectsDir(), self.name)


    def syncToDisk(self):
        return self.createOnDisk()

    def createOnDisk(self):
        self._createBaseDirs()
        self._createConfigs()
        self._createAssets()
        self._createShots()

        return self._validateFileStructure()

    def _createBaseDirs(self):
        ## Create main project
        projectRoot = self.path 
        
        if not os.path.exists(projectRoot):
            os.mkdir(projectRoot)

        ## Create all root dirs
        basedirs = ["assets",
                    "shots",
                    "config",
                    "sandbox"]
        for directory in basedirs:
            makedir = os.path.join(projectRoot, directory)
            if not os.path.exists(makedir):
                os.mkdir(makedir)

    def _createConfigs(self):
        data = self.serialize()

        self._backupConfigs()

        with open(self._mainConfigFilePath(), "w") as outfile:
            json.dump(data, outfile, indent=4)

    def _mainConfigFilePath(self):
        return os.path.join(self.path, "config", Project.mainConfigFileName())

    def _backupConfigs(self):
        if not os.path.exists(self.configDir):
            return False
        
        backupFolder = os.path.join(self.configDir, "backup", datetime.datetime.now().isoformat())
        for filename in [x for x in os.listdir(self.configDir) if os.path.isdir(os.path.join(self.configDir,x))]:
            os.copy(os.path.join(self.configDir,filename), os.path.join(backupFolder, filename))

    def _createAssets(self):
        for asset in self.assets.values():
            asset.createOnDisk()

    def _createShots(self):
        for shot in self.shots.values():
            shot.createOnDisk()

    def _validateFileStructure(self):
        return os.path.exists(self.path)
 
