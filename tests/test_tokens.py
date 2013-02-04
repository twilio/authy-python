import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from authy import AuthyException
from authy.api.resources import Token
from authy.api.resources import Tokens
from authy.api.resources import User
from authy.api.resources import Users


class TokensTest(unittest.TestCase):

    def setUp(self):
        self.users = Users("http://sandbox-api.authy.com", 'bf12974d70818a08199d17d5e2bae630')
        self.resource = Tokens("http://sandbox-api.authy.com", 'bf12974d70818a08199d17d5e2bae630')

    def test_verify_invalid_token(self):
        user = self.users.create('test@example.com', '345-782-4988', 1)
        token = self.resource.verify(user.id, 'token')
        self.assertIsInstance(token, Token)
        self.assertFalse(token.ok())
        self.assertEqual(token.errors()['token'], 'is invalid')

    def test_verify_valid_token(self):
        user = self.users.create('test@example.com', '345-782-4988', 1)
        token = self.resource.verify(user.id, '0000000')
        self.assertIsInstance(token, Token)
        self.assertTrue(token.ok())

    def test_force_verify_token(self):
        user = self.users.create('test@example.com', '345-782-4988', 1)
        token = self.resource.verify(user.id, '0000000', {"force": True})
        self.assertIsInstance(token, Token)
        self.assertTrue(token.ok())
