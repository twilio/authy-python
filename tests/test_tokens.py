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
        user_id = test_helper.API_USER_ID
        with self.assertRaises(AuthyFormatException) as context:
            token = self.resource.verify(user_id, 'token')

        self.assertTrue('Invalid Token. Only digits accepted.' in str(context.exception))

    def test_verify_digits_authy_id(self):
        user_id = test_helper.API_USER_ID
        with self.assertRaises(AuthyFormatException) as context:
            token = self.resource.verify('user_id', '123456')

        self.assertTrue('Invalid Authy id. Only digits accepted.' in str(context.exception))

    def test_verify_longer_token(self):
        user_id = test_helper.API_USER_ID
        with self.assertRaises(AuthyFormatException) as context:
            token = self.resource.verify(user_id, '0000000111111')

        self.assertTrue('Invalid Token. Unexpected length.' in str(context.exception))

    def test_verify_invalid_token(self):
        user_id = test_helper.API_USER_ID
        token = self.resource.verify(user_id, '1111111')
        self.assertIsInstance(token, Token)
        self.assertFalse(token.ok())
        self.assertEqual(token.errors()['message'], 'Token is invalid')
        self.assertEqual(token.response.status_code, 401)

    def test_verify_valid_token(self):
        user_id = test_helper.API_USER_ID
        token = self.resource.verify(user_id, '0000000')
        self.assertIsInstance(token, Token)
        self.assertEqual(token.errors(), {})
        self.assertTrue(token.ok())

    def test_force_verify_token(self):
        user_id = test_helper.API_USER_ID
        token = self.resource.verify(user_id, '0000000', {"force": True})
        self.assertIsInstance(token, Token)
        self.assertEqual(token.errors(), {})
        self.assertTrue(token.ok())

if __name__ == "__main__":
	    unittest.main()
