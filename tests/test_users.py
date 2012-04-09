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
        self.resource = Users("http://localhost:4567", 'testing_python_api_key')

    def test_create_valid_user(self):
        user = self.resource.create('test@example.com', '3457824988', 1)
        self.assertIsInstance(user, User)
        self.assertTrue(user.ok())
        self.assertTrue('user' in user.content)
    
    def test_create_invalid_user(self):
        user = self.resource.create('testexample.com', '782392032', 1)
        
        self.assertFalse(user.ok())
        self.assertIsInstance(user, User)
        self.assertTrue('email' in user.content)
        self.assertEqual(user.content['email'], ['is invalid'])

