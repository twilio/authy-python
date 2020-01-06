import six
import sys
import test_helper
import unittest

if six.PY3:
    from unittest.mock import MagicMock
else:
    from mock import MagicMock

from authy.api.resources import OneTouch
from authy.api.resources import OneTouchResponse
from authy import AuthyException

class OneTouchTest(unittest.TestCase):

    def setUp(self):
        self.resource = MagicMock(
            OneTouch(test_helper.API_URL, test_helper.API_KEY))
        self.response = MagicMock()
        otr = MagicMock(OneTouchResponse(self.resource, self.response))
        otr.errors = MagicMock(return_value={})
        otr.ok = MagicMock(return_value=True)
        otr.get_uuid = MagicMock(
            return_value="1836762c-e4b7-4c99-a0e4-d8e7518b4e78")
        otr.status = MagicMock(return_value=True)

        self.resource.send_request = MagicMock(return_value=otr)
        self.resource.get_approval_status = MagicMock(return_value=otr)
        self.resource.clean_logos = OneTouch.clean_logos
        self.resource.__make_http_query = OneTouch._OneTouch__make_http_query
        self.resource.validate_one_touch_signature = OneTouch.validate_one_touch_signature
        self.resource.api_key = 'foobar123'

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

        logos = [dict(res='default', url='https://www.python.org/static/img/python-logo.png'),
                 dict(res='low', url='https://www.python.org/static/img/python-logo.png')]

        push_response = self.resource.send_request(
            user_id, message, seconds_to_expire, details, hidden_details, logos)

        self.assertIsInstance(push_response, OneTouchResponse)
        self.resource.send_request.assert_called_with(
            user_id, message, seconds_to_expire, details, hidden_details, logos)
        self.assertEqual(push_response.errors(), {})
        self.assertTrue(push_response.ok())
        self.assertIsNotNone(push_response.get_uuid())
        self.assertTrue(self.resource.get_approval_status(
            push_response.get_uuid()).status())

    def test_send_request_with_minimum_data(self):
        user_id = test_helper.AUTH_ID_A
        message = "Login requested for a CapTrade Bank account."
        touch = self.resource.send_request(user_id, message)

        self.assertIsInstance(touch, OneTouchResponse)
        self.assertEqual(touch.errors(), {})
        self.assertTrue(touch.ok())
        self.assertIsNotNone(touch.get_uuid())
        self.assertNotEqual(self.resource.get_approval_status(
            touch.get_uuid()).status(), False)

    def test_validate_request_blank_user_id(self):
        self.resource._validate_request = OneTouch._validate_request

        user_id = ''
        message = "Login requested for a CapTrade Bank account."

        with self.assertRaises(AuthyException) as context:
            self.resource._validate_request(self.resource, user_id, message)

        self.assertEqual(
            "Invalid authy id, user id is requred and must be an integer value.", str(context.exception))

    def test_validate_request_blank_message(self):
        self.resource._validate_request = OneTouch._validate_request

        user_id = test_helper.AUTH_ID_A
        message = ''

        with self.assertRaises(AuthyException) as context:
            self.resource._validate_request(self.resource, user_id, message)

        self.assertEqual(
            "Invalid message - should not be empty. It is required", str(context.exception))

    def test_send_request_with_blank_user_id(self):
        user_id = ''
        message = "Login requested for a CapTrade Bank account."

        def side_effect(user_id, message):
            if user_id == '':
                raise AuthyException()

        self.resource.send_request.side_effect = side_effect

        with self.assertRaises(AuthyException) as context:
            self.resource.send_request(user_id, message)

        self.resource.send_request.assert_called_with('', message)
        self.resource._validate_request.assert_called_once

    def test_send_request_with_blank_message(self):
        user_id = test_helper.AUTH_ID_A
        message = ''

        def side_effect(user_id, message):
            if message == '':
                raise AuthyException()

        self.resource.send_request.side_effect = side_effect

        with self.assertRaises(AuthyException) as context:
            self.resource.send_request(user_id, message)

        self.resource.send_request.assert_called_with(14125, '')
        self.resource._validate_request.assert_called_once

    def test_clean_logos_invalid_key(self):
        logos = [dict(wrong='default', url='https://www.python.org/static/img/python-logo.png'),
                 dict(res='low', url='https://www.python.org/static/img/python-logo.png')]

        with self.assertRaises(AuthyException) as context:
            self.resource.clean_logos(self.resource, logos)

        self.assertEqual(
            "Invalid logos list. Only res and url required", str(context.exception))

    def test_clean_logos_invalid_data_type(self):
        logos = dict(
            res='default', url='https://www.python.org/static/img/python-logo.png')

        with self.assertRaises(AuthyException) as context:
            self.resource.clean_logos(self.resource, logos)

        self.assertEqual(
            "Invalid logos list. Only res and url required", str(context.exception))

    def test_ONETOUCH_CALLBACK_CHECK_WD_POST_METHOD(self):
        touch = self.resource.validate_one_touch_signature(self.resource,
                                                           test_helper.POST_REQ_SIGNATURE,
                                                           test_helper.NONCE,
                                                           "POST",
                                                           test_helper.URL,
                                                           test_helper.PARAMS)
        self.assertIsInstance(touch, bool)
        self.assertEqual(touch, True)

    def test_ONETOUCH_CALLBACK_CHECK_WD_POST_METHOD_INVAILED_NONCE(self):
        touch = self.resource.validate_one_touch_signature(self.resource,
                                                           test_helper.POST_REQ_SIGNATURE,
                                                           'INVAILED NONCE',
                                                           "POST",
                                                           test_helper.URL,
                                                           test_helper.PARAMS)
        self.assertIsInstance(touch, bool)
        self.assertEqual(touch, False)

    def test_ONETOUCH_CALLBACK_CHECK_WD_GET_METHOD(self):
        touch = self.resource.validate_one_touch_signature(self.resource,
                                                           test_helper.GET_REQ_SIGNATURE,
                                                           test_helper.NONCE,
                                                           "GET",
                                                           test_helper.URL,
                                                           test_helper.PARAMS)
        self.assertIsInstance(touch, bool)
        self.assertEqual(touch, True)

    def test_ONETOUCH_CALLBACK_CHECK_WD_GET_METHOD_INVAILED_NONCE(self):
        touch = self.resource.validate_one_touch_signature(self.resource,
                                                           test_helper.GET_REQ_SIGNATURE,
                                                           'INVAILED NONCE',
                                                           "GET",
                                                           test_helper.URL,
                                                           test_helper.PARAMS)
        self.assertIsInstance(touch, bool)
        self.assertEqual(touch, False)


if __name__ == "__main__":
    unittest.main()
