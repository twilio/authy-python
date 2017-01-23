import sys
import test_helper

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from authy import AuthyException
from authy.api.resources import oneTouchResponse
from authy.api.resources import oneTouch


class oneTouchTest(unittest.TestCase):

    def setUp(self):
        self.resource = oneTouch(test_helper.LIVE_API_URL, test_helper.LIVE_API_KEY)

    def test_send_request_with_valid_data(self):
        details = {}
        details['username'] = 'example@example.com'
        details['location'] = 'California, USA'
        details['Account Number'] = 'YOUR ACCOUNT NUMBER'
        logos= {}
        hidden_details = {}
        hidden_details['ip_address'] = '110.37.200.52'

        user_id = "YOUR USER ID"
        message = "Login requested for a CapTrade Bank account."
        seconds_to_expire = 120

        onetouch = self.resource.send_request(user_id, message, seconds_to_expire, details, hidden_details, logos)
        self.assertIsInstance(onetouch, oneTouchResponse)
        self.assertTrue(onetouch.ok())
        self.assertEqual(onetouch.errors(), {})
        self.assertNotEqual(onetouch.get_uuid(), None, 'some error in sent_rquest.')
        self.assertNotEqual(self.resource.get_approval_status(onetouch.get_uuid()).status(), False, 'Some error in request.')

    def test_send_request_with_in_valid_data(self):
        details = {}
        details['username'] = 'example@example.com'
        details['location'] = 'California, USA'
        details['Account Number'] = ''
        logos= {}
        hidden_details = {}
        hidden_details['ip_address'] = '110.37.200.52'

        user_id = ""
        message = "Login requested for a CapTrade Bank account."
        seconds_to_expire = 120

        onetouch = self.resource.send_request(user_id, message, seconds_to_expire, details, hidden_details, logos)
        self.assertIsInstance(onetouch, oneTouchResponse)
        self.assertNotEqual(onetouch.ok(), True)
        self.assertNotEqual(onetouch.errors(), {})
        self.assertEqual(onetouch.get_uuid(), None)
        self.assertEqual(self.resource.get_approval_status(onetouch.get_uuid()).status(), False)

if __name__ == "__main__":
	    unittest.main()
