import requests
import platform
import six

# * ApiClient

#  Python 2.7/3.4
#
#  :category Services
#  :package  Authy
#  :author   David Cuadrado <david@authy.com>
#  :license  http://creativecommons.org/licenses/MIT/ MIT
#  :link     https://github.com/authy/authy-python

# Authy API interface.
# :category Services
# :package  Authy
# :author   David Cuadrado < david @ authy.com >
# :license  http: // creativecommons.org / licenses / MIT / MIT
# :link     https://github.com/authy/authy-python

from authy import __version__, AuthyFormatException
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

# import json
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        from django.utils import simplejson as json


class Resource(object):
    """
    Request CRUD defined in Resouce.
    """
    def __init__(self, api_uri, api_key):
        """
        Class constructor
        :param string api_uri:
        :param string api_key:
        """
        self.api_uri = api_uri
        self.api_key = api_key
        self.def_headers = self.__default_headers()

    def post(self, path, data={}):
        """
        initiate create request to client server.
        :param string path:
        :param dict data Receives from child class:
        :return json response:
        """
        return self.request("POST", path, data, {'Content-Type': 'application/json'})

    def get(self, path, data={}):
        """
        initiate get request to client server.
        :param string path:
        :param dict data:
        :return Json response:
        """
        return self.request("GET", path, data)

    def put(self, path, data={}):
        """
        initiate update request.
        :param string path:
        :param dict data:
        :return:
        """
        return self.request("PUT", path, data, {'Content-Type': 'application/json'})

    def delete(self, path, data={}):
        """
        initiate recored delete request.
        :param string path:
        :param dict data:
        :return:
        """
        return self.request("DELETE", path, data)

    def request(self, method, path, data={}, headers={}):
        """

        :param callback method:
        :param string path:
        :param dict data:
        :param headers:
        :return:
        """
        url = self.api_uri + path
        params = {}
        temp = headers.copy()
        if six.PY3:
            temp = dict(
                self.def_headers.items() |
                headers.items()
            )
        else:
            temp = dict(
                self.def_headers.items() +
                headers.items()
            )
        headers = temp
        headers['X-Authy-API-Key'] = self.api_key
        if method == "GET":
            params.update(data)
            return requests.request(method, url, headers=headers, params=params)
        else:
            return requests.request(method, url, headers=headers, params=params, data=json.dumps(data))

    def __default_headers(self):
        platform_value = ""
        try:
          platform_value = platform.platform(True)
        except:
          platform_value = "unknown_platform"

        return {
            'User-Agent': "AuthyPython/{0} ({1}; Python {2})".format(
                __version__,
                platform.platform(True),
                platform.python_version()
            )}


class Instance(object):
    """
    Response parsing from resource request api calls
    """
    def __init__(self, resource, response):
        """
        Class constructor.
        :param class instance resource:
        :param class instance response:
                """
        self.resource = resource
        self.response = response

        try:
            self.content = self.response.json()
        except ValueError:
            self.content = self.response.text

    def ok(self):
        """

        :return Response code(200) if success:
        """
        return self.response.status_code == 200

    def errors(self):
        """
        :return error dict if no success:
        """
        if self.ok():
            return {}

        errors = self.content

        if(not isinstance(errors, dict)):
            errors = {"error": errors}  # convert to dict for consistency
        elif('errors' in errors):
            errors = errors['errors']

        return errors

    def __getitem__(self, key):
        return self.content[key]


class Sms(Instance):
    """
    sms response handler
    """
    def ignored(self):
        try:
            self.content['ignored']
            return True
        except KeyError:
            return False


class User(Instance):
    """
    users class response handler.
    """
    def __init__(self, resource, response):
        """
        user constructor. assigns id if exist.
        :param resource class instance:
        :param response class instance:
        """
        super(User, self).__init__(resource, response)
        if(isinstance(self.content, dict) and 'user' in self.content):
            self.id = self.content['user']['id']
        else:
            self.id = None


class Users(Resource):
    """
    create, check status or delete user through this users datatype
    """
    def create(self, email, phone, country_code=1):
        """
        sends request to create new user.
        :param string email:
        :param string phone:
        :param string country_code:
        :return:
        """
        data = {
            "user": {
                "email": email,
                "cellphone": phone,
                "country_code": country_code
            }
        }

        resp = self.post("/protected/json/users/new", data)

        return User(self, resp)

    def request_sms(self, user_id, options={}):
        resp = self.get("/protected/json/sms/" + quote(str(user_id)), options)

        return Sms(self, resp)

    def status(self, user_id):
        resp = self.get("/protected/json/users/{0}/status".format(user_id))

        return User(self, resp)

    def delete(self, user_id):
        resp = self.post("/protected/json/users/{0}/delete".format(user_id))

        return User(self, resp)


class Token(Instance):

    def ok(self):
        if super(Token, self).ok():
            return '"token":"is valid"' in str(self.response.content)
        return False


class Tokens(Resource):

    def verify(self, device_id, token, options={}):
        self.__validate(token, device_id)
        if 'force' not in options:
            options['force'] = "true"
        resp = self.get(
            "/protected/json/verify/{}/{}".format(quote(str(token)), quote(str(device_id))), options)
        return Token(self, resp)

    def __validate(self, token, device_id):
        self.__validate_digit(token, "Invalid Token. Only digits accepted.")
        self.__validate_digit(
            device_id, "Invalid Authy id. Only digits accepted.")
        length = len(token)
        if length < 6 or length > 10:
            raise AuthyFormatException("Invalid Token. Unexpected length.")

    def __validate_digit(self, var, message):
        if six.PY3:
            if not isinstance(var, (int)) and not var.isdigit():
                raise AuthyFormatException(message)
        else:
            if not isinstance(var, (int, long)) and not var.isdigit():
                raise AuthyFormatException(message)


class App(Instance):
    pass


class Apps(Resource):

    def fetch(self):
        resp = self.get("/protected/json/app/details")
        return App(self, resp)


class Stats(Instance):
    pass


class StatsResource(Resource):

    def fetch(self):
        resp = self.get("/protected/json/app/stats")
        return Stats(self, resp)


class Phone(Instance):
    pass


class Phones(Resource):

    def verification_start(self, phone_number, country_code, via='sms', locale=None):
        """

        :param string phone_number stored in your databse or you provided while creating new user.:
        :param string country_code stored in your databse or you provided while creating new user.:
        :param string via verification method either sms or call:
        :param string locale optional default none:
        :return:
        """
        options = {
            'phone_number': phone_number,
            'country_code': country_code,
            'via': via
        }

        if locale:
            options['locale'] = locale

        resp = self.post("/protected/json/phones/verification/start", options)
        return Phone(self, resp)

    def verification_check(self, phone_number, country_code, verification_code):
        """

        :param phone_number:
        :param country_code:
        :param verification_code:
        :return:
        """
        options = {
            'phone_number': phone_number,
            'country_code': country_code,
            'verification_code': verification_code
        }
        resp = self.get("/protected/json/phones/verification/check", options)
        return Phone(self, resp)

    def info(self, phone_number, country_code):
        options = {
            'phone_number': phone_number,
            'country_code': country_code
        }
        resp = self.get("/protected/json/phones/info", options)
        return Phone(self, resp)
    
class oneTouchResponse(Instance):
    """
    oneTouch response handler.
    """
    def __init__(self, resource, response):
        """
        oneTouchResponse constructor. receives two prams
        :param resource instance:
        :param response of oneTouch datatype:
        """
        self.status_code = None;
        super(oneTouchResponse, self).__init__(resource, response)
        if (isinstance(self.content, dict) and 'approval_request' in self.content):
            self.uuid = self.content['approval_request']['uuid']
        else:
            self.uuid = None

    def getUuid(self):
        return self.uuid


class oneTouch(Resource):
    def send_request(self, user_id, message,seconds_to_expire=120,details={},hidden_details={}, logos={}):
        """
        OneTouch verification request. Sends a request for Auth App. For more info https://www.twilio.com/docs/api/authy/authy-onetouch-api
        :param string user_id: user_id User's authy id stored in your database
        :param string message: Required, the message shown to the user when the approval request arrives.
        :param number seconds_to_expire: Optional, defaults to 120 (two minutes).
        :param dict details:  For example details['Requested by'] = 'MacBook Pro, Chrome'; it will be displayed on Authy app
        :param dict hidden_details: Same usage as detail except this detail is not shown in Authy app
        :param dict logos: Contains the logos that will be shown to user. The logos parameter is expected to be an array of objects, each object with two fields: res (values are default,low,med,high) and url
        :return oneTouchResponse: the server response Json Object
        """
        encode_logos = []
        if len(logos):
            for logo in logos:
                l = {
                    'res': quote(logo.get('res', '')),
                    'url': quote(logo.get('url', ''))
                }
                encode_logos.append(l)

        data = {
            "message": message,
            "seconds_to_expire": seconds_to_expire,
            "details": details,
            'hidden_details': hidden_details,
            'logos': encode_logos

        }
        request_url = "/onetouch/json/users/{0}/approval_requests".format(user_id)
        response = self.post(request_url, data)
        return oneTouchResponse(self, response)

    def get_approval_status(self, uuid):
        """
        OneTouch verification request. Sends a request for Auth App. For more info https://www.twilio.com/docs/api/authy/authy-onetouch-api
        :param string uuid Required. The approval request ID. (Obtained from the response to an ApprovalRequest):
        :return oneTouchResponse the server response Json Object:
        """
        request_url = "/onetouch/json/approval_requests/{0}".format(uuid)
        response = self.get(request_url)
        return (response.json())



