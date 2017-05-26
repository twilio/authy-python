import sys
import test_helper

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

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
        self.assertRegexpMatches(phone['message'], 'Text message sent')

    def test_verification_start(self):
        phone = self.phones.verification_start(self.phone_number, self.country_code)
        self.assertTrue(phone.ok(), msg="errors: {0}".format(phone.errors()))
        self.assertRegexpMatches(phone['message'], 'Text message sent')

    def test_verification_check_incorrect_code(self):
        phone = self.phones.verification_check(self.phone_number, self.country_code, '1234')
        self.assertFalse(phone.ok(), msg="errors: {0}".format(phone.errors()))
        self.assertRegexpMatches(phone.errors()['message'], 'Verification code is incorrect.')

    def test_verification_check(self):
        self.phones.verification_start(self.phone_number, self.country_code)
        phone = self.phones.verification_check(self.phone_number, self.country_code, '0000')
        self.assertTrue(phone.ok(), msg="errors: {0}".format(phone.errors()))
        self.assertRegexpMatches(phone['message'], 'Verification code is correct')

    def test_phone_info(self):
        phone = self.phones.info(self.phone_number, self.country_code)
        self.assertTrue(phone.ok(), msg="errors: {0}".format(phone.errors()))
        self.assertRegexpMatches(phone['message'], 'Phone number information as of')
        self.assertRegexpMatches(phone['type'], 'landline')
        self.assertFalse(phone['ported'])

if __name__ == "__main__":
	    unittest.main()
