import sys
import test_helper

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from unittest.mock import patch, Mock
from authy import AuthyException
from authy.api import AuthyApiClient
from authy.api.resources import Phones
from authy.api.resources import Phone


class PhonesTest(unittest.TestCase):

    def setUp(self):
        self.api = AuthyApiClient(test_helper.API_KEY, test_helper.API_URL)
        self.phones = Phones(test_helper.API_URL, test_helper.API_KEY)
        self.phone_number = test_helper.PHONE_NUMBER
        self.country_code = test_helper.COUNTRY_CODE

    def test_phones(self):
        self.assertIsInstance(self.api.phones, Phones)

    def test_verification_start_without_via(self):
        phone = self.phones.verification_start(self.phone_number, self.country_code,'sms')
        self.assertTrue(phone.ok(), msg="errors: {0}".format(phone.errors()))
        self.assertRegex(phone['message'], 'Text message sent')

    def test_verification_start(self):
        phone = self.phones.verification_start(self.phone_number, self.country_code)
        self.assertTrue(phone.ok(), msg="errors: {0}".format(phone.errors()))
        self.assertRegex(phone['message'], 'Text message sent')

    @patch('authy.api.resources.Phones')
    def test_verification_check_incorrect_code(self, MockPhones):
        phones = MockPhones()
        phones.verification_check.side_effect = lambda x,y,z: {'0000': 'Verification code is correct.', '1234': 'Verification code is incorrect.'}[z]

        response = phones.verification_check(self.phone_number, self.country_code, '1234')
        self.assertEqual(response, 'Verification code is incorrect.')


    @patch('authy.api.resources.Phones')
    def test_verification_check(self, MockPhones):
        phones = MockPhones()
        phones.verification_check.side_effect = lambda x,y,z: {'0000': 'Verification code is correct.', '1234': 'Verification code is incorrect.'}[z]

        response = phones.verification_check(self.phone_number, self.country_code, '0000')
        self.assertEqual(response, 'Verification code is correct.')

    def test_phone_info(self):
        phone = self.phones.info(self.phone_number, self.country_code)
        self.assertTrue(phone.ok(), msg="errors: {0}".format(phone.errors()))
        self.assertRegex(phone['message'], 'Phone number information as of')
        self.assertRegex(phone['type'], 'landline')
        self.assertFalse(phone['ported'])

if __name__ == "__main__":
	    unittest.main()
