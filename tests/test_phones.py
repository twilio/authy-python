import six
import sys
import test_helper
import unittest

if six.PY3:
    from unittest.mock import MagicMock
else:
    from mock import MagicMock

from authy import AuthyException, AuthyFormatException
from authy.api import AuthyApiClient
from authy.api.resources import Phones
from authy.api.resources import Phone


class PhonesTest(unittest.TestCase):

    def setUp(self):
        
        self.phones = MagicMock(Phones(test_helper.API_URL, test_helper.API_KEY))
        self.response = MagicMock()

        phone = MagicMock(Phone(self.phones, self.response))
        phone.ok = MagicMock(return_value=True)
        phone.errors = MagicMock(return_value={})

        self.phone_number = test_helper.PHONE_NUMBER
        self.country_code = test_helper.COUNTRY_CODE

        self.phones.__validate_channel = Phones._Phones__validate_channel
        self.phones.__validate_code_length = Phones._Phones__validate_code_length
        self.phones.verification_start = MagicMock(return_value = phone)


    def test_phones(self):
        self.assertIsInstance(self.phones, Phones)

    def test_verification_start(self):
        phone = self.phones.verification_start(
            self.phone_number, self.country_code)
        self.assertTrue(phone.ok())
        self.assertEqual(phone.errors(), {})

    def test_verification_start_with_code_length(self):
        cl = self.phones.__validate_code_length(self.phones, code_length=7)
        self.assertEqual(cl, 7)

    def test_verification_start_with_str_code_length(self):
        cl = self.phones.__validate_code_length(self.phones, code_length='7')
        self.assertEqual(cl, 7)

    def test_verification_start_with_non_numeric_code_length(self):
        self.assertRaises(AuthyFormatException,
                          self.phones.__validate_code_length,
                          self.phones,
                          code_length='foo')

    def test_verification_start_with_too_short_code_length(self):
        self.assertRaises(AuthyFormatException,
                          self.phones.__validate_code_length,
                          self.phones,
                          code_length=2)

    def test_verification_start_with_too_long_code_length(self):
        self.assertRaises(AuthyFormatException,
                          self.phones.__validate_code_length,
                          self.phones,
                          code_length=12)


if __name__ == "__main__":
    unittest.main()
