import six
import sys
import test_helper
import unittest

if six.PY3:
    from unittest.mock import MagicMock
else:
    from mock import MagicMock

from authy import AuthyException
from authy.api.resources import User, Sms
from authy.api.resources import Users
from authy.api import AuthyApiClient


class UsersTest(unittest.TestCase):

    def setUp(self):
        self.users = MagicMock(Users(test_helper.API_URL, test_helper.API_KEY))
        self.response = MagicMock()
        
        user = MagicMock(User(self.users, self.response))
        user.content = {"user": {"id": test_helper.API_USER_ID}, "success": True, "message": "something"}
        user.errors = MagicMock(return_value={})
        user.ok = MagicMock(return_value=True)
        user.id = MagicMock(return_value=test_helper.API_USER_ID)

        sms = MagicMock(Sms(self.users, self.response))
        sms.errors = MagicMock(return_value={})

        self.users.create = MagicMock(return_value = user)
        self.users.delete = MagicMock(return_value = user)
        self.users.status = MagicMock(return_value = user)
        self.users.request_sms = MagicMock(return_value = sms)

    def test_users(self):
        self.assertIsInstance(self.users, Users)

    def test_create_valid_user(self):
        user = self.users.create('test@example.com', '3457824988', 1)
        self.assertEqual(user.errors(), {})
        self.assertIsInstance(user, User)
        self.assertTrue(user.ok())
        self.assertTrue('user' in user.content)
        self.assertIsNotNone(user.id)

    def test_request_sms_token(self):
        user = self.users.create('test@example.com', '202-555-0158', 1)
        sms = self.users.request_sms(user.id)
        self.assertTrue(sms.ok())
        self.assertTrue(sms.content['success'])
        self.assertEqual(sms.errors(), {})
        self.assertEqual(user.errors(), {})

    def test_sms_ignored(self):
        user = self.users.create('test@example.com', '202-555-0197', 1)
        sms = self.users.request_sms(user.id)
        self.assertTrue(sms.ok())
        # fake 'ignored' field in JSON response
        sms.content['ignored'] = 'true'
        self.assertTrue(sms.ignored())

    def test_get_user_status(self):
        user = self.users.create('test@example.com', '3107810860', 1)
        status = self.users.status(user.id)
        self.assertTrue(status.ok(), msg="errors: {0}".format(status.errors()))
        self.assertTrue(status.content['success'])
        self.assertEqual(status.errors(), {})

    def test_delete_user(self):
        user = self.users.create('test@example.com', '3107810860', 1)
        user = self.users.delete(user.id)
        self.assertTrue(user.ok())
        self.assertTrue(user.content['success'])
        self.assertEqual(user.errors(), {})

if __name__ == "__main__":
	    unittest.main()
