
import sys
import test_helper

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from authy.api import AuthyApiClient
from authy.api.resources import OneTouchRequests

from .fakeauthy import FakeAuthyAPIServer


class OneTouchTest(unittest.TestCase):

    def setUp(self):

        self.api = AuthyApiClient(test_helper.FAKE_AUTHY_URL, test_helper.API_URL)
        self.one_touch = OneTouchRequests(test_helper.FAKE_AUTHY_URL, test_helper.API_KEY)

        self.authy_server = FakeAuthyAPIServer(port=test_helper.FAKE_AUTHY_PORT)
        self.authy_server.start()

        self.uuid = '12345678-aaaa-0123-8888-005a6b7c8d9e'
        self.user_id = '12345678'
        self.message = 'Approve'

    def tearDown(self):
        self.authy_server.stop()

    def test_one_touch(self):
        self.assertIsInstance(self.api.one_touch, OneTouchRequests)

    def test_initiate_approval_request(self):

        response = {'approval_request': {'uuid': self.uuid}, 'success': True}
        self.authy_server.set_response(response=response, code=200)

        request = self.one_touch.initiate_approval_request(user_id=self.user_id, message=self.message)
        self.assertTrue(request.ok())
        self.assertEquals(request.content, response)
        self.assertEquals(request.errors(), {})
        self.assertEquals(request.status, None)

    def test_initiate_approval_request_user_not_found(self):

        response = {'message': 'User not found.', 'success': False,
                    'errors': {'message': 'User not found.'}, 'error_code': '60026'}
        self.authy_server.set_response(response=response, code=404)

        request = self.one_touch.initiate_approval_request(user_id=self.user_id, message=self.message)
        self.assertFalse(request.ok())
        self.assertEquals(request.content, response)
        self.assertEquals(request.errors(), response['errors'])

    def test_approval_request_status(self):

        status = 'pending'

        response = {'approval_request':
                        {'_app_name': 'Test',
                         '_app_serial_id': 12345,
                         '_authy_id': self.user_id,
                         '_id': 'aaaaaaaaaaaaaaaaaaaaaaaa',
                         '_user_email': 'test@example.com',
                         'app_id': 'aaaaaaaaaaaaaaaaaaaaaaaa',
                         'created_at': '2016-12-01T10:10:01Z',
                         'notified': False,
                         'processed_at': None,
                         'seconds_to_expire': 84000,
                         'status': status,
                         'updated_at': '2016-12-01T10:10:01Z',
                         'user_id': 'aaaaaaaaaaaaaaaaaaaaaaaa',
                         'uuid': self.uuid},
                    'success': True}

        self.authy_server.set_response(response=response, code=200)
        request = self.one_touch.approval_request_status(uuid=self.uuid)

        self.assertTrue(request.ok())
        self.assertEquals(request.content, response)
        self.assertEquals(request.errors(), {})
        self.assertEquals(request.status, status)

    def test_approval_request_status_uuid_not_found(self):

        bad_uuid = 'a'
        response = {'message': 'Approval request not found: {0}'.format(bad_uuid),
                    'success': False, 'errors': {}, 'error_code': '60049'}
        self.authy_server.set_response(response=response, code=404)
        request = self.one_touch.approval_request_status(uuid=self.uuid)

        self.assertFalse(request.ok())
        self.assertEquals(request.content, response)
        self.assertEquals(request.errors(), response['errors'])
        self.assertEquals(request.status, None)


if __name__ == "__main__":

    unittest.main()
