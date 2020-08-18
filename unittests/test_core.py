import unittest

from core import Asset, Shot

class TestCreate(unittest.TestCase):
    def test_demo(self):
        tmp = "foo"

    def test_name(self):
        asset = Asset("troll")
        self.assertEquals(asset.name, "troll")

    @unittest.expectedFailure
    def test_nameImmutable(self):
        asset = Asset("foo")
        asset.name = "bar"

class TestSerialize(unittest.TestCase):
    def test_shot(self):
        shot = Shot("fx010")
        expected = {
                        "name": "fx010"
                    }
        self.assertEquals(shot.serialize(), expected)

    def test_asset(self):
        asset = Asset("troll")
        expected = {
                        "name": "troll"
                    }
        self.assertEquals(asset.serialize(), expected)
