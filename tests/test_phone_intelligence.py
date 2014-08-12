import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from authy import AuthyException
from authy.api import AuthyApiClient
from authy.api.resources import PhoneIntelligence
from authy.api.resources import PhoneInfo

class PhoneIntelligenceTest(unittest.TestCase):

    def setUp(self):
        #self.api = AuthyApiClient("authy_website_key", "http://localhost:4567")
        #self.phone_intelligence = PhoneIntelligence("http://localhost:4567", 'authy_website_key')

        self.api = AuthyApiClient("bf12974d70818a08199d17d5e2bae630", "http://sandbox-api.authy.com")
        self.phone_intelligence = PhoneIntelligence("http://sandbox-api.authy.com", 'bf12974d70818a08199d17d5e2bae630')

    def test_phone_intelligence(self):
        self.assertIsInstance(self.api.phone_intelligence, PhoneIntelligence)

    def test_verification_start_without_country_code(self):
        phone_info = self.phone_intelligence.verification_start({
            'via': 'sms',
            'phone_number': '111-111-1111'
        })
        self.assertFalse(phone_info.ok())
        self.assertRegexpMatches(phone_info.errors()['message'], 'Country code is mandatory')

    def test_verification_start(self):
        phone_info = self.phone_intelligence.verification_start({
            'via': 'sms',
            'country_code': '1',
            'phone_number': '111-111-1111'
        })
        self.assertTrue(phone_info.ok(), msg="errors: {0}".format(phone_info.errors()))
        self.assertRegexpMatches(phone_info['message'], 'Text message sent')

    def test_verification_check_incorrect_code(self):
        phone_info = self.phone_intelligence.verification_check({
            'country_code': '1',
            'phone_number': '111-111-1111',
            'verification_code': '1234'
        })
        self.assertFalse(phone_info.ok(), msg="errors: {0}".format(phone_info.errors()))
        self.assertRegexpMatches(phone_info.errors()['message'], 'Verification code is incorrect.')

    def test_verification_check(self):
        phone_info = self.phone_intelligence.verification_check({
            'country_code': '1',
            'phone_number': '111-111-1111',
            'verification_code': '0000'
        })
        self.assertTrue(phone_info.ok(), msg="errors: {0}".format(phone_info.errors()))
        self.assertRegexpMatches(phone_info['message'], 'Verification code is correct')

    def test_phone_info(self):
        phone_info = self.phone_intelligence.info({
            'country_code': '1',
            'phone_number': '7754615609'
        })
        self.assertTrue(phone_info.ok(), msg="errors: {0}".format(phone_info.errors()))
        self.assertRegexpMatches(phone_info['message'], 'Phone number information as of')
        self.assertRegexpMatches(phone_info['type'], 'voip')
        self.assertRegexpMatches(phone_info['provider'], 'Google Voice')
        self.assertFalse(phone_info['ported'])
