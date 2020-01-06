import six
import sys
import test_helper
import unittest

if six.PY3:
    from unittest.mock import MagicMock
else:
    from mock import MagicMock

from authy import AuthyException, AuthyFormatException
from authy.api.resources import Token
from authy.api.resources import Tokens
from authy.api.resources import User
from authy.api.resources import Users
from authy.api.resources import OneTouch


class TokensTest(unittest.TestCase):

    def setUp(self):
        self.resource = MagicMock(Tokens(test_helper.API_URL, test_helper.API_KEY))
        self.response = MagicMock()

        token = MagicMock(Token(self.resource, self.response))
        token.ok = MagicMock(return_value=True)
        token.errors = MagicMock(return_value={})

        self.resource.__validate_digit = Tokens._Tokens__validate_digit
        self.resource.__validate = Tokens._Tokens__validate

    def test_verify_digits_token(self):
        with self.assertRaises(AuthyFormatException) as context:
            self.resource.__validate_digit(self.resource, var='token', message='parroted')

        self.assertTrue('parroted' in str(context.exception))

    def test_verify_longer_token(self):
        user_id = test_helper.API_USER_ID
        with self.assertRaises(AuthyFormatException) as context:
            self.resource.__validate(self.resource, token='0000000111111', device_id=user_id)

        self.assertTrue('Invalid Token. Unexpected length.' in str(context.exception))

if __name__ == "__main__":
	    unittest.main()
