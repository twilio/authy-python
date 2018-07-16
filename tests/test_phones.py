import sys
import test_helper

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from mockito import when, mock

from authy import AuthyException, AuthyFormatException
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
        self.assertEquals(phone['message'], 'Text message sent to +1 305-456-2345.')

    def test_verification_start(self):
        phone = self.phones.verification_start(self.phone_number, self.country_code)
        self.assertTrue(phone.ok(), msg="errors: {0}".format(phone.errors()))
        self.assertEquals(phone['message'], 'Text message sent to +1 305-456-2345.')

    def test_verification_start_with_code_length(self):
        phone = self.phones.verification_start(self.phone_number, self.country_code,
                                               code_length=7)
        self.assertTrue(phone.ok(), msg="errors: {0}".format(phone.errors()))
        self.assertRegexpMatches(phone['message'], 'Text message sent')

    def test_verification_start_with_str_code_length(self):
        phone = self.phones.verification_start(self.phone_number, self.country_code,
                                               code_length='7')
        self.assertTrue(phone.ok(), msg="errors: {0}".format(phone.errors()))
        self.assertRegexpMatches(phone['message'], 'Text message sent')

    def test_verification_start_with_non_numeric_code_length(self):
        self.assertRaises(AuthyFormatException,
                          self.phones.verification_start,
                          self.phone_number,
                          self.country_code,
                          code_length='foo')

    def test_verification_start_with_too_short_code_length(self):
        self.assertRaises(AuthyFormatException,
                          self.phones.verification_start,
                          self.phone_number,
                          self.country_code,
                          code_length=2)

    def test_verification_start_with_too_long_code_length(self):
        self.assertRaises(AuthyFormatException,
                          self.phones.verification_start,
                          self.phone_number,
                          self.country_code,
                          code_length=12)

    def test_verification_check_incorrect_code(self):
        when(self.phones).verification_check(self.phone_number, self.country_code, '1234').thenReturn(
            'Verification code is incorrect.')

        response = self.phones.verification_check(self.phone_number, self.country_code, '1234')
        self.assertEqual(response, 'Verification code is incorrect.')

    def test_verification_check(self):
        when(self.phones).verification_check(self.phone_number, self.country_code, '0000').thenReturn(
            'Verification code is correct.')

        response = self.phones.verification_check(self.phone_number, self.country_code, '0000')
        self.assertEqual(response, 'Verification code is correct.')

    def test_phone_info(self):
        phone = self.phones.info(self.phone_number, self.country_code)
        self.assertTrue(phone.ok(), msg="errors: {0}".format(phone.errors()))
        self.assertTrue('Phone number information as of' in phone['message'])
        self.assertEquals(phone['type'], 'landline')
        self.assertFalse(phone['ported'])

if __name__ == "__main__":
	    unittest.main()
