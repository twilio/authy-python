import sys
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
        self.api = AuthyApiClient("bf12974d70818a08199d17d5e2bae630", "http://sandbox-api.authy.com")
        self.phones = Phones("http://sandbox-api.authy.com", 'bf12974d70818a08199d17d5e2bae630')

    def test_phones(self):
        self.assertIsInstance(self.api.phones, Phones)

    def test_verification_start_without_via(self):
        phone = self.phones.verification_start('111-111-1111', '1')
        self.assertTrue(phone.ok(), msg="errors: {0}".format(phone.errors()))
        self.assertRegexpMatches(phone['message'], 'Text message sent')

    def test_verification_start(self):
        phone = self.phones.verification_start('111-111-1111', '1', 'sms')
        self.assertTrue(phone.ok(), msg="errors: {0}".format(phone.errors()))
        self.assertRegexpMatches(phone['message'], 'Text message sent')

    def test_verification_check_incorrect_code(self):
        phone = self.phones.verification_check('111-111-1111', '1', '1234')
        self.assertFalse(phone.ok(), msg="errors: {0}".format(phone.errors()))
        self.assertRegexpMatches(phone.errors()['message'], 'Verification code is incorrect.')

    def test_verification_check(self):
        phone = self.phones.verification_check('111-111-1111', '1', '0000')
        self.assertTrue(phone.ok(), msg="errors: {0}".format(phone.errors()))
        self.assertRegexpMatches(phone['message'], 'Verification code is correct')

    def test_phone_info(self):
        phone = self.phones.info('7754615609', '1')
        self.assertTrue(phone.ok(), msg="errors: {0}".format(phone.errors()))
        self.assertRegexpMatches(phone['message'], 'Phone number information as of')
        self.assertRegexpMatches(phone['type'], 'voip')
        self.assertRegexpMatches(phone['provider'], 'Google Voice')
        self.assertFalse(phone['ported'])
