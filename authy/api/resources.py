import requests
from urllib import quote

# import json
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        from django.utils import simplejson as json


class Resource(object):
    def __init__(self, api_uri, api_key):
        self.api_uri = api_uri
        self.api_key = api_key

    def post(self, path, data = {}):
        return self.request("POST", path, data, {'Content-Type': 'application/json'})

    def get(self, path, data = {}):
        return self.request("GET", path, data)

    def put(self, path, data = {}):
        return self.request("PUT", path, data, {'Content-Type': 'application/json'})

    def delete(self, path, data = {}):
        return self.request("DELETE", path, data)

    def request(self, method, path, data = {}, headers = {}):
        url = self.api_uri + path
        params = {"api_key": self.api_key}

        if method == "GET":
            params.update(data)
            return requests.request(method, url, headers=headers, params=params)
        else:
            return requests.request(method, url, headers=headers, params=params, data=json.dumps(data))


class Instance(object):
    def __init__(self, resource, response):
        self.resource = resource
        self.response = response

        try:
            self.content = self.response.json()
        except ValueError:
            self.content = self.response.text

    def ok(self):
        return self.response.status_code == 200

    def errors(self):
        if self.ok():
            return {}

        errors = self.content

        if(not isinstance(errors, dict)):
            errors = {"error": errors} # convert to dict for consistency
        elif('errors' in errors):
            errors = errors['errors']

        return errors

    def __getitem__(self, key):
        return self.content[key]


class User(Instance):
    def __init__(self, resource, response):
        super(User, self).__init__(resource, response)
        if(isinstance(self.content, dict) and 'user' in self.content):
            self.id = self.content['user']['id']
        else:
            self.id = None


class Users(Resource):
    def create(self, email, phone, country_code = 1):
        data = {
            "user": {
                "email": email,
                "cellphone": phone,
                "country_code": country_code
            }
        }

        resp = self.post("/protected/json/users/new", data)

        return User(self, resp)

    def request_sms(self, user_id, options = {}):
        resp = self.get("/protected/json/sms/"+quote(str(user_id)), options)

        return Instance(self, resp)

    def status(self, user_id):
        resp = self.get("/protected/json/users/{0}/status".format(user_id))

        return User(self, resp)


class Token(Instance):
    pass


class Tokens(Resource):
    def verify(self, device_id, token, options = {}):
        if 'force' not in options:
            options['force'] = "true"
        resp = self.get("/protected/json/verify/"+quote(str(token))+"/"+quote(str(device_id)), options)
        return Token(self, resp)


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
    def verification_start(self, phone_number, country_code, via = 'sms'):
        options = {
            'phone_number': phone_number,
            'country_code': country_code,
            'via': via
        }
        resp = self.post("/protected/json/phones/verification/start", options)
        return Phone(self, resp)

    def verification_check(self, phone_number, country_code, verification_code):
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
