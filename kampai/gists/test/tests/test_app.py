
from KAMPAI_PACKAGE_NAME.app import App

import unittest


class TestApp(unittest.TestCase):

    def test_app_creation(self):

        app = App()

        self.assertTrue(type(app) == App)
