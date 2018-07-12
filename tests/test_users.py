import sys
import test_helper

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from authy import AuthyException
from authy.api.resources import User
from authy.api.resources import Users
from authy.api import AuthyApiClient


class UsersTest(unittest.TestCase):

    def setUp(self):
        self.api = AuthyApiClient(test_helper.API_KEY, test_helper.API_URL)
        self.users = Users(test_helper.API_URL, test_helper.API_KEY)

    def test_users(self):
        self.assertIsInstance(self.api.users, Users)

    def test_create_valid_user(self):
        user = self.users.create('test@example.com', '3457824988', 1)
        self.assertEqual(user.errors(), {})
        self.assertIsInstance(user, User)
        self.assertTrue(user.ok())
        self.assertTrue('user' in user.content)
        self.assertIsNotNone(user.id)

    def test_create_invalid_user(self):
        user = self.users.create('testexample.com', '782392032', 1)

        self.assertFalse(user.ok())
        self.assertIsInstance(user, User)
        self.assertEqual(user.errors()['email'], 'is invalid')
        self.assertIsNone(user.id)

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
