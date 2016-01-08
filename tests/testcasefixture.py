from infoblox import infoblox
import unittest
import os


class TestCaseWithFixture(unittest.TestCase):
    location = os.path.dirname(__file__)
    fixture_name = None

    @classmethod
    def setUpClass(cls):
        super(TestCaseWithFixture, cls).setUpClass()
        cls.body = cls.load_fixture(cls.fixture_name)
        cls.iba_ipa = infoblox.Infoblox('10.10.10.10', 'foo', 'bar',
                                        '1.6', 'default', 'default')

    @classmethod
    def load_fixture(cls, fixture_name):
        filename = "{}/data/{}.json".format(cls.location,
                                            cls.fixture_name)
        with open(filename, 'r') as file:
            return file.read()
