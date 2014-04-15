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
