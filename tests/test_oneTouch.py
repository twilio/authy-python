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
        user_id = test_helper.AUTH_ID_A
        message = "Login requested for a CapTrade Bank account."
        seconds_to_expire = 120

        details = {}
        details['username'] = 'example@example.com'
        details['location'] = 'California, USA'
        details['Account Number'] = test_helper.AUTH_ID_B

        hidden_details = {}
        hidden_details['ip_address'] = '110.37.200.52'

        logos = [dict(res='default', url='https://www.python.org/static/img/python-logo.png'), dict(res='low', url='https://www.python.org/static/img/python-logo.png')]


        touch = self.resource.send_request(user_id, message, seconds_to_expire, details, hidden_details, logos)
        self.assertIsInstance(touch, oneTouchResponse)
        self.assertTrue(touch.ok())
        self.assertEqual(touch.errors(), {})
        self.assertIsNotNone(touch.get_uuid())
        self.assertNotEqual(self.resource.get_approval_status(touch.get_uuid()).status(), False)

    def test_send_request_with_balnk_userId(self):
        user_id = ''
        message = "Login requested for a CapTrade Bank account."
        seconds_to_expire = 120

        details = {}
        details['username'] = 'example@example.com'
        details['location'] = 'California, USA'
        details['Account Number'] = test_helper.AUTH_ID_B

        hidden_details = {}
        hidden_details['ip_address'] = '110.37.200.52'

        logos = [dict(res='default', url='https://www.python.org/static/img/python-logo.png'),
                 dict(res='low', url='https://www.python.org/static/img/python-logo.png')]

        touch = self.resource.send_request(user_id, message, seconds_to_expire, details, hidden_details, logos)
        self.assertIsInstance(touch, oneTouchResponse)
        self.assertEqual(touch.ok(), False)
        self.assertEqual(touch.errors(), {'error': '{"message": "user_id is missing"}'})
        self.assertEqual(touch.get_uuid(), False)

    def test_send_request_with_balnk_message(self):
        user_id = test_helper.AUTH_ID_A
        message = ''
        seconds_to_expire = 120

        details = {}
        details['username'] = 'example@example.com'
        details['location'] = 'California, USA'
        details['Account Number'] = test_helper.AUTH_ID_B

        hidden_details = {}
        hidden_details['ip_address'] = '110.37.200.52'

        logos = [dict(res='default', url='https://www.python.org/static/img/python-logo.png'),
                 dict(res='low', url='https://www.python.org/static/img/python-logo.png')]

        touch = self.resource.send_request(user_id, message, seconds_to_expire, details, hidden_details, logos)
        self.assertIsInstance(touch, oneTouchResponse)
        self.assertEqual(touch.ok(), False)
        self.assertEqual(touch.errors(), {'error': '{"message": "Message is missing."}'})
        self.assertEqual(touch.get_uuid(), False)

    def test_send_request_with_balnk_details(self):
        user_id = test_helper.AUTH_ID_A
        message = 'Some test message' 
        seconds_to_expire = 120

        details = {}

        hidden_details = {}
        hidden_details['ip_address'] = '110.37.200.52'

        logos = [dict(res='default', url='https://www.python.org/static/img/python-logo.png'),
                 dict(res='low', url='https://www.python.org/static/img/python-logo.png')]

        touch = self.resource.send_request(user_id, message, seconds_to_expire, details, hidden_details, logos)
        self.assertIsInstance(touch, oneTouchResponse)
        self.assertEqual(touch.ok(), False)
        self.assertEqual(touch.errors(), {'error': '{"message": "Sender\'s account details are missing."}'})
        self.assertEqual(touch.get_uuid(), False)

    def test_send_request_with_inValid_logoKey(self):
        user_id = test_helper.AUTH_ID_A
        message = 'Test Message'
        seconds_to_expire = 120

        details = {}
        details['username'] = 'example@example.com'
        details['location'] = 'California, USA'
        details['Account Number'] = test_helper.AUTH_ID_B

        hidden_details = {}
        hidden_details['ip_address'] = '110.37.200.52'

        logos = [dict(wrong='default', url='https://www.python.org/static/img/python-logo.png'),
                 dict(res='low', url='https://www.python.org/static/img/python-logo.png')]

        touch = self.resource.send_request(user_id, message, seconds_to_expire, details, hidden_details, logos)
        self.assertIsInstance(touch, oneTouchResponse)
        self.assertEqual(touch.ok(), False)
        self.assertEqual(touch.errors(), {'error': '{"message": "Invalid logos dict keys. Expected \'res\' or \'url\'"}'})
        self.assertEqual(touch.get_uuid(), False)

    def test_send_request_with_inValid_logo_dataType(self):
        user_id = test_helper.AUTH_ID_A
        message = 'Test Message'
        seconds_to_expire = 120

        details = {}
        details['username'] = 'example@example.com'
        details['location'] = 'California, USA'
        details['Account Number'] = test_helper.AUTH_ID_B

        hidden_details = {}
        hidden_details['ip_address'] = '110.37.200.52'

        logos = dict(res='default', url='https://www.python.org/static/img/python-logo.png')


        touch = self.resource.send_request(user_id, message, seconds_to_expire, details, hidden_details, logos)
        self.assertIsInstance(touch, oneTouchResponse)
        self.assertEqual(touch.ok(), False)
        self.assertNotEqual(touch.errors(), {})
        self.assertEqual(touch.get_uuid(), False)

    def test_send_request_with_blank_hidden_details(self):
        user_id = test_helper.AUTH_ID_A
        message = 'Test Message'
        seconds_to_expire = 120

        details = {}
        details['username'] = 'example@example.com'
        details['location'] = 'California, USA'
        details['Account Number'] = test_helper.AUTH_ID_B

        hidden_details = {}

        logos = [dict(wrong='default', url='https://www.python.org/static/img/python-logo.png'),
                 dict(res='low', url='https://www.python.org/static/img/python-logo.png')]

        touch = self.resource.send_request(user_id, message, seconds_to_expire, details, hidden_details, logos)
        self.assertIsInstance(touch, oneTouchResponse)
        self.assertEqual(touch.ok(), False)
        self.assertEqual(touch.errors(), {'error': '{"message": "Hidden details can\'t blank."}'})
        self.assertEqual(touch.get_uuid(), False)

if __name__ == "__main__":
	    unittest.main()
