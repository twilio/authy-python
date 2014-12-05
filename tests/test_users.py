import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from authy import AuthyException
from authy.api.resources import User
from authy.api.resources import Users


class UsersTest(unittest.TestCase):

    def setUp(self):
        self.resource = Users("http://sandbox-api.authy.com", 'bf12974d70818a08199d17d5e2bae630')

    def test_create_valid_user(self):
        user = self.resource.create('test@example.com', '3457824988', 1)
        self.assertIsInstance(user, User)
        self.assertTrue(user.ok())
        self.assertTrue('user' in user.content)
        self.assertIsNotNone(user.id)
        self.assertEqual(user.errors(), {})

    def test_create_invalid_user(self):
        user = self.resource.create('testexample.com', '782392032', 1)

        self.assertFalse(user.ok())
        self.assertIsInstance(user, User)
        self.assertEqual(user.errors()['email'], 'is invalid')
        self.assertIsNone(user.id)

    def test_request_sms_token(self):
        user = self.resource.create('test@example.com', '3107810860', 1)
        sms = self.resource.request_sms(user.id)
        self.assertTrue(sms.ok())
        self.assertTrue(sms.content['success'])
        self.assertEqual(sms.errors(), {})
        self.assertEqual(user.errors(), {})

    def test_sms_ignored(self):
        user = self.resource.create('test@example.com', '3107810860', 1)
        sms = self.resource.request_sms(user.id)
        self.assertTrue(sms.ok())
        # fake 'ignored' field in JSON response
        sms.content['ignored'] = 'true'
        self.assertTrue(sms.ignored())

    def test_get_user_status(self):
        user = self.resource.create('test@example.com', '3107810860', 1)
        status = self.resource.status(user.id)
        self.assertTrue(status.ok(), msg="errors: {0}".format(status.errors()))
        self.assertTrue(status.content['success'])
        self.assertEqual(status.errors(), {})

    def test_delete_user(self):
        user = self.resource.create('test@example.com', '3107810860', 1)
        user = self.resource.delete(user.id)
        self.assertTrue(user.ok())
        self.assertTrue(user.content['success'])
        self.assertEqual(user.errors(), {})
