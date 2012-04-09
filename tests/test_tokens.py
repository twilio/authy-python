import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from authy import AuthyException
from authy.api.resources import Token
from authy.api.resources import Tokens


class TokensTest(unittest.TestCase):

    def setUp(self):
        self.resource = Tokens("http://localhost:4567", 'testing_python_api_key')

    def test_verify_token(self):
        token = self.resource.verify('1', 'token')
        self.assertIsInstance(token, Token)
        self.assertFalse(token.ok())
        self.assertEqual(token.content, 'invalid key')

