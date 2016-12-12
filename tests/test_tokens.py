import sys
import test_helper

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from authy import AuthyException, AuthyFormatException
from authy.api.resources import Token
from authy.api.resources import Tokens
from authy.api.resources import User
from authy.api.resources import Users


class TokensTest(unittest.TestCase):

    def setUp(self):
        self.users = Users(test_helper.API_URL, test_helper.API_KEY)
        self.resource = Tokens(test_helper.API_URL, test_helper.API_KEY)

    def test_verify_digits_token(self):
        user = self.users.create('test@example.com', '310-781-0860', 1)
        try:
            token = self.resource.verify(user.id, 'token')
            self.fail()
        except Exception, e:
            self.assertIsInstance(e, AuthyFormatException)
            self.assertEqual(e.message, 'Invalid Token. Only digits accepted.')

    def test_verify_digits_authy_id(self):
        user = self.users.create('test@example.com', '310-781-0860', 1)
        try:
            token = self.resource.verify('user.id', '0000000')
            self.fail()
        except Exception, e:
            self.assertIsInstance(e, AuthyFormatException)
            self.assertEqual(e.message, 'Invalid Authy id. Only digits accepted.')

    def test_verify_longer_token(self):
        user = self.users.create('test@example.com', '202-555-0166', 1)
        try:
            token = self.resource.verify(user.id, '00000001111')
            self.fail()
        except Exception, e:
            self.assertIsInstance(e, AuthyFormatException)
            self.assertEqual(e.message, 'Invalid Token. Unexpected length.')

    def test_verify_invalid_token(self):
        user = self.users.create('test@example.com', '202-555-0166', 1)
        token = self.resource.verify(user.id, '1111111')
        self.assertIsInstance(token, Token)
        self.assertFalse(token.ok())
        self.assertEqual(token.response.status_code, 401)
        self.assertEqual(token.errors()['message'], 'Token is invalid')

    def test_verify_valid_token(self):
        user = self.users.create('test@example.com', '202-555-0166', 1)
        token = self.resource.verify(user.id, '0000000')
        self.assertIsInstance(token, Token)
        self.assertTrue(token.ok())

    def test_force_verify_token(self):
        user = self.users.create('test@example.com', '202-555-0166', 1)
        token = self.resource.verify(user.id, '0000000', {"force": True})
        self.assertIsInstance(token, Token)
        self.assertTrue(token.ok())

if __name__ == "__main__":
        unittest.main()
