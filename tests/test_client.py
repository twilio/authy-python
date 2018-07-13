import sys
import test_helper
import six

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
        self.api = AuthyApiClient(test_helper.API_KEY, test_helper.API_URL)

    def test_tokens(self):
        self.assertIsInstance(self.api.tokens, Tokens)

    def test_users(self):
        self.assertIsInstance(self.api.users, Users)

    def test_version(self):
        if six.PY3:
            self.assertRegex(self.api.version(), '\d.\d*')
        else:
            import re
            self.assertTrue(re.compile(r'\d.\d*').search(self.api.version()))


if __name__ == "__main__":
	    unittest.main()
