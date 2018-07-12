import sys
import test_helper

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from authy import AuthyException
from authy.api.resources import OneTouchResponse
from authy.api.resources import OneTouch


class OneTouchTest(unittest.TestCase):

    def setUp(self):
        self.resource = OneTouch(test_helper.LIVE_API_URL, test_helper.LIVE_API_KEY)

    def test_send_request_with_valid_data(self):
        user_id = test_helper.AUTH_ID_A
        message = "Login requested for a CapTrade Bank account."
        seconds_to_expire = 120

        details = {}
        details['username'] = 'example@example.com'
        details['location'] = 'California, USA'
        details['Account Number'] = '8675309'

        hidden_details = {}
        hidden_details['ip_address'] = '110.37.200.52'

        logos = [dict(res='default', url='https://www.python.org/static/img/python-logo.png'), dict(res='low', url='https://www.python.org/static/img/python-logo.png')]

        touch = self.resource.send_request(user_id, message, seconds_to_expire, details, hidden_details, logos)
        self.assertIsInstance(touch, OneTouchResponse)
        self.assertEqual(touch.errors(), {})
        self.assertTrue(touch.ok())
        self.assertIsNotNone(touch.get_uuid())
        self.assertNotEqual(self.resource.get_approval_status(touch.get_uuid()).status(), False)

    def test_send_request_with_minimum_data(self):
        user_id = test_helper.AUTH_ID_A
        message = "Login requested for a CapTrade Bank account."
        touch = self.resource.send_request(user_id, message)

        self.assertIsInstance(touch, OneTouchResponse)
        self.assertEqual(touch.errors(), {})
        self.assertTrue(touch.ok())
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

        try:
            touch = self.resource.send_request(user_id, message, seconds_to_expire, details, hidden_details, logos)
        except AuthyException as e:
            self.assertEqual(str(e), "Invalid authy id, user id is requred and must be an integer value.")

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
        try:
            touch = self.resource.send_request(user_id, message, seconds_to_expire, details, hidden_details, logos)
        except AuthyException as e:
            self.assertEqual(str(e), "Invalid message - should not be empty. It is required")

    def test_send_request_with_blank_details(self):
        user_id = test_helper.AUTH_ID_A
        message = 'Some test message'
        seconds_to_expire = 120

        details = {}

        hidden_details = {}
        hidden_details['ip_address'] = '110.37.200.52'

        logos = [dict(res='default', url='https://www.python.org/static/img/python-logo.png'),
                 dict(res='low', url='https://www.python.org/static/img/python-logo.png')]

        try:
            touch = self.resource.send_request(user_id, message, seconds_to_expire, details, hidden_details, logos)
        except AuthyException as e:
            self.assertEqual(str(e), "Invalid details - should not be empty. It is required")

    def test_send_request_with_invalid_logoKey(self):
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

        try:
            touch = self.resource.send_request(user_id, message, seconds_to_expire, details, hidden_details, logos)
        except AuthyException as e:
            self.assertEqual(str(e), "Invalid logos list. Only res and url required")

    def test_send_request_with_invalid_logo_dataType(self):
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


        try:
            touch = self.resource.send_request(user_id, message, seconds_to_expire, details, hidden_details, logos)
        except AuthyException as e:
            self.assertEqual(str(e), "Invalid logos list. Only res and url required")


    def test_ONETOUCH_CALLBACK_CHECK_WD_POST_MEHTHOD(self):

        touch = self.resource.validate_one_touch_signature(test_helper.POST_REQ_SIGNATURE,
                                                           test_helper.NONCE,
                                                           "POST",
                                                           test_helper.URL,
                                                           test_helper.PARAMS)
        self.assertIsInstance(touch, bool)
        self.assertEqual(touch, True)

    def test_ONETOUCH_CALLBACK_CHECK_WD_POST_MEHTHOD_INVAILED_NONCE(self):

        touch = self.resource.validate_one_touch_signature(test_helper.POST_REQ_SIGNATURE,
                                                           'INVAILED NONCE',
                                                           "POST",
                                                           test_helper.URL,
                                                           test_helper.PARAMS)
        self.assertIsInstance(touch, bool)
        self.assertEqual(touch, False)

    def test_ONETOUCH_CALLBACK_CHECK_WD_GET_METHOD(self):
        touch = self.resource.validate_one_touch_signature(test_helper.GET_REQ_SIGNATURE,
                                                           test_helper.NONCE,
                                                           "GET",
                                                           test_helper.URL,
                                                           test_helper.PARAMS)
        self.assertIsInstance(touch, bool)
        self.assertEqual(touch, True)

    def test_ONETOUCH_CALLBACK_CHECK_WD_GET_METHOD_INVAILED_NONCE(self):
        touch = self.resource.validate_one_touch_signature(test_helper.GET_REQ_SIGNATURE,
                                                           'INVAILED NONCE',
                                                           "GET",
                                                           test_helper.URL,
                                                           test_helper.PARAMS)
        self.assertIsInstance(touch, bool)
        self.assertEqual(touch, False)

if __name__ == "__main__":
	    unittest.main()
