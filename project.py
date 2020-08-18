import logging
import os
import json
import datetime

from core import Asset, Shot

logger = logging.getLogger(__name__)

class Project:
    def __init__(self, name):
        self._name = name
        if self._isProjectOnDisk():
            self._initFromDisk()
        else:
            self.shots = {}
            self.assets = {}

    def _initFromDisk(self):
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
        self.shots[shot.name] = shot

    def addAsset(self, asset):
        ## TODO: Check for string vs Asset object
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
        return self.name in self.listProjects()

    def createOnDisk(self):
        if self._isProjectOnDisk:
            logger.warning("Can't create project {} on disk, it already exists".format(self.name))
            return False

        self._createBaseDirs()
        self._createConfigs()
        self._createAssets()
        self._createShots()

        return self._validateFileStructure()

    def _createBaseDirs(self):
        ## Create main project
        projectRoot = os.path.join(Project.rootDir(), self.name)
        
        if os.path.exists(projectRoot):
            logger.error("Project directory already exists")
            raise Exception

        os.mkdir(projectRoot)

        ## Create all root dirs
        basedirs = ["assets",
                    "shots",
                    "config",
                    "sandbox"]
        for directory in basedirs:
            os.mkdir(os.path.join(projectRoot, directory))

    def _createConfigs(self):
        data = self.serialize()

        self._backupConfigs()

        with open(self._mainConfigFilePath, "w") as outfile:
            json.dump(data, outfile, indent=4)

    def _mainConfigFilePath(self):
        return os.path.join(self.rootDir, "config", Project.mainConfigFileName)

    def _backupConfigs(self):
        configFolder = os.path.join(self.rootDir, "config")
        if not os.path.exists(configFolder):
            return False
        
        backupFolder = os.path.join(configFolder, "backup", datetime.datetime.now().isoformat())
        for filename in [x for x in os.listDir(configFolder) if os.path.isdir(os.path.join(configFolder,x))]:
            os.copy(os.path.join(configFolder,filename), os.path.join(backupFolder, filename))

    def _createAssets(self):
        for asset in self.assets.values():
            asset.createOnDisk()

    def _createShots(self):
        for shot in self.shots.values():
            shot.createOnDisk()

    def _validateFileStructure(self):
        projectRoot = os.path.join(Project.rootDir(), self.name)
        return os.path.exists(projectRoot)
 
