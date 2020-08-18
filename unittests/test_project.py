import unittest

from project import *

class TestCreate(unittest.TestCase):
    def test_demo(self):
        tmp = "foo"

    def test_exists(self):
        ## test if a project exists or not
        project = Project("unittest")
        self.assertTrue(project.exists)

        project2 = Project("foo")
        self.assertFalse(project2.exists)

    def test_serialize(self):
        project = Project("foo")
        shots = ["fx010", "fx020", "fo100"]
        assets = ["foo", "bar", "troll"]
        expected = {
                    "name": "foo",
                    "shots": {},
                    "assets": {}
                    }
        for shot in [Shot(x) for x in shots]:
            project.addShot(shot)
            expected["shots"][shot.name] = {"name": shot.name}

        for asset in [Asset(x) for x in assets]:
            project.addAsset(asset)
            expected["assets"][asset.name] = {"name": asset.name}

        self.assertEqual(project.serialize(), expected)

