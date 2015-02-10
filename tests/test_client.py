import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from authy import AuthyException
from authy.api import AuthyApiClient
from authy.api.resources import Tokens
from authy.api.resources import Users


class ApiClientTest(unittest.TestCase):

    def setUp(self):
        self.api = AuthyApiClient("bf12974d70818a08199d17d5e2bae630", "http://sandbox-api.authy.com")

    def test_tokens(self):
        self.assertIsInstance(self.api.tokens, Tokens)

    def test_users(self):
        self.assertIsInstance(self.api.users, Users)

    def test_version(self):
    	self.assertRegexpMatches(self.api.version(), '\d.\d*')
