import requests
import platform
import six
import hashlib, hmac, base64, re

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

MIN_TOKEN_SIZE = 6
MAX_TOKEN_SIZE = 12
MAX_STRING_SIZE = 200

try:
    _PLAT_STR = platform.platform(True)
except IOError:
    _PLAT_STR = "unknown_platform"

class Resource(object):
    """
    Request CRUD defined in Resource.
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
        return {
            'User-Agent': "AuthyPython/{0} ({1}; Python {2})".format(
                __version__,
                _PLAT_STR,
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

        :return Response True if success:
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

class Call(Instance):
    """
    call response handler
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
    def create(self, email, phone, country_code=1, send_install_link_via_sms=False):
        """
        sends request to create new user.
        :param string email:
        :param string phone:
        :param string country_code:
        :param bool send_install_link_via_sms:
        :return:
        """
        data = {
            "user": {
                "email": email,
                "cellphone": phone,
                "country_code": country_code
            },

            'send_install_link_via_sms': send_install_link_via_sms
        }

        resp = self.post("/protected/json/users/new", data)

        return User(self, resp)

    def request_sms(self, user_id, options={}):
        resp = self.get("/protected/json/sms/" + quote(str(user_id)), options)

        return Sms(self, resp)

    def request_call(self, user_id, options={}):
        resp = self.get("/protected/json/call/" + quote(str(user_id)), options)

        return Call(self, resp)

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
            "/protected/json/verify/{0}/{1}".format(quote(str(token)), quote(str(device_id))), options)
        return Token(self, resp)

    def __validate(self, token, device_id):
        self.__validate_digit(token, "Invalid Token. Only digits accepted.")
        self.__validate_digit(
            device_id, "Invalid Authy id. Only digits accepted.")
        length = len(token)
        if length < MIN_TOKEN_SIZE or length > MAX_TOKEN_SIZE:
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

    def verification_start(self, phone_number, country_code, via='sms',
                           locale=None, code_length=4):
        """
        :param string phone_number: stored in your databse or you provided while creating new user.
        :param string country_code: stored in your databse or you provided while creating new user.
        :param string via: verification method either sms or call
        :param string locale: optional default none
        :param number code_length: optional default 4
        :return:
        """

        if via != 'sms' and via != 'call':
            raise AuthyFormatException("Invalid Via. Expected 'sms' or 'call'.")

        options = {
            'phone_number': phone_number,
            'country_code': country_code,
            'via': via
        }

        if locale:
            options['locale'] = locale

        try:
            cl = int(code_length)
            if cl < 4 or cl > 10:
                raise ValueError
            options['code_length'] = cl
        except ValueError:
            raise AuthyFormatException("Invalid code_length. Expected numeric value from 4-10.")

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

class OneTouchResponse(Instance):
    """
    OneTouch response handler.
    """
    def __init__(self, resource, response):
        """
        OneTouchResponse constructor. receives two prams
        :param resource instance:
        :param response of OneTouch datatype:
        """
        self.uuid = None
        super(OneTouchResponse, self).__init__(resource, response)
        if (isinstance(self.content, dict) and 'approval_request' in self.content):
            self.uuid = self.content['approval_request']['uuid']


    def get_uuid(self):
        if not self.uuid:
            return False
        return self.uuid

    def status(self):
        success = False

        if ('success' in self.content):
            success = self.content['success']

        return success


class OneTouch(Resource):

    def send_request(self, user_id, message, seconds_to_expire=None, details={}, hidden_details={}, logos=[]):
        """
        OneTouch verification request. Sends a request for Auth App. For more info https://www.twilio.com/docs/api/authy/authy-onetouch-api
        :param string user_id: user_id User's authy id stored in your database
        :param string message: Required, the message shown to the user when the approval request arrives.
        :param number seconds_to_expire: Optional, defaults to 120 (two minutes).
        :param dict details:  For example details['Requested by'] = 'MacBook Pro, Chrome'; it will be displayed on Authy app
        :param dict hidden_details: Same usage as detail except this detail is not shown in Authy app
        :param list logos: Contains the logos that will be shown to user. The logos parameter is expected to be an array of objects, each object with two fields: res (values are default,low,med,high) and url
        :return OneTouchResponse: the server response Json Object
        """

        if not user_id or not isinstance(user_id, int):
            raise AuthyFormatException('Invalid authy id, user id is requred and must be an integer value.')

        if not message:
            raise AuthyFormatException('Invalid message - should not be empty. It is required')

        data = {
            "message": message[:MAX_STRING_SIZE],
            "seconds_to_expire": seconds_to_expire,
            "details":self.__clean_inputs(details),
            'hidden_details': self.__clean_inputs(hidden_details),
            'logos': self.clean_logos(logos)
        }

        request_url = "/onetouch/json/users/{0}/approval_requests".format(user_id)
        response = self.post(request_url, data)
        return OneTouchResponse(self, response)


    def clean_logos(self, logos):
        """
        Validate logos input.
        :param list logos:
        :return list logos:
        """
        if not len(logos):
            return logos # Allow nil hash
        if not isinstance(logos, list):
            raise AuthyFormatException('Invalid logos list. Only res and url required')

        temp_array = {}
        clean_logos = []

        for logo in logos:

            if not isinstance(logo, dict):
                raise AuthyFormatException('Invalid logo type')

            for l in logo:
                # We ignore any additional parameter on the logos, and truncate
                # string size to the maximum allowed.
                if l == 'res':
                    temp_array['res'] = logo[l][:MAX_STRING_SIZE]
                elif l == 'url':
                    temp_array['url'] = logo[l][:MAX_STRING_SIZE]
                else:
                    raise AuthyFormatException('Invalid logos list. Only res and url required')

            clean_logos.append(temp_array)
            temp_array = {}

        return clean_logos

    def get_approval_status(self, uuid):
        """
        OneTouch verification request. Sends a request for Auth App. For more info https://www.twilio.com/docs/api/authy/authy-onetouch-api
        :param string uuid Required. The approval request ID. (Obtained from the response to an ApprovalRequest):
        :return OneTouchResponse the server response Json Object:
        """
        request_url = "/onetouch/json/approval_requests/{0}".format(uuid)
        response = self.get(request_url)
        return OneTouchResponse(self,response)

    def validate_one_touch_signature(self, signature, nonce, method, url, params):
        """
        Function to validate signature in X-Authy-Signature key of headers.

        :param string signature: X-Authy-Signature key of headers.
        :param string nonce: X-Authy-Signature-Nonce key of headers.
        :param string method: GET or POST - configured in app settings for OneTouch.
        :param string url: base callback url.
        :param dict params: params sent by Authy.
        :return bool: True if calculated signature and X-Authy-Signature are identical else False.
        """
        if not signature or not isinstance(signature, str):
            raise AuthyFormatException("Invalid signature - should not be empty. It is required")

        if not nonce:
            raise AuthyFormatException("Invalid nonce - should not be empty. It is required")

        if not method or not ('get' == method.lower() or 'post' == method.lower() ):
            raise AuthyFormatException("Invalid method - should not be empty. It is required")

        if not params or not isinstance(params, dict):
            raise AuthyFormatException("Invalid params - should not be empty. It is required")


        query_params = self.__make_http_query(params)
        # Sort and replace encoded  params in case-sensitive order
        sorted_params = '&'.join(sorted(query_params.replace('/', '%2F').replace('%20', '+').split('&')))
        sorted_params = re.sub("\\%5B([0-9])*\\%5D","%5B%5D",sorted_params)
        sorted_params = re.sub("\\=None", "=", sorted_params)
        data = nonce + "|" + method + "|" + url + "|" + sorted_params
        try:
            calculated_signature = base64.b64encode(hmac.new(self.api_key.encode(), data.encode(), hashlib.sha256).digest())
            return calculated_signature.decode() == signature
        except:
            calculated_signature = base64.b64encode(hmac.new(self.api_key, data, hashlib.sha256).digest())
            return calculated_signature == signature

    def __make_http_query(self, params, topkey=''):
        """
        Function to covert params into url encoded query string
        :param dict params: Json string sent  by Authy.
        :param string topkey: params key
        :return string: url encoded Query.
        """
        if len(params) == 0:
            return ""
        result = ""
        # is a dictionary?
        if type(params) is dict:
            for key in params.keys():
                newkey = quote(key)
                if topkey != '':
                    newkey = topkey + quote('[' + key + ']')
                if type(params[key]) is dict:
                    result += self.__make_http_query(params[key], newkey)
                elif type(params[key]) is list:
                    i = 0
                    for val in params[key]:
                        if type(val) is dict:
                            result +=   self.__make_http_query(val, newkey + quote('['+str(i)+']'))
                        else:
                            result += newkey + quote('['+str(i)+']') + "=" + quote(str(val)) + "&"
                        i = i + 1
                # boolean should have special treatment as well
                elif type(params[key]) is bool:
                    result += newkey + "=" + quote(str(params[key]).lower()) + "&"
                # assume string (integers and floats work well)
                else:
                    result += newkey + "=" + quote(str(params[key])) + "&"
        # remove the last '&'
        if (result) and (topkey == '') and (result[-1] == '&'):
            result = result[:-1]
        return result


    def __clean_inputs(self, params):

        if not isinstance(params, dict):
            return params[:MAX_STRING_SIZE]

        temp_hash = {}

        for k in params:
            if not isinstance(params[k], dict):
                temp_hash[k[:MAX_STRING_SIZE]] = params[k][:MAX_STRING_SIZE]
            else:
                temp_hash[k[:MAX_STRING_SIZE]] = self.__clean_inputs(params[k]);

        return temp_hash
