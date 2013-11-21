import re
import datetime
import logging
import authy
from authy import AuthyException
from authy import AuthyApiException
from urllib import urlencode, quote
from urlparse import urlparse

# import json
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        from django.utils import simplejson as json

# import httplib2
try:
    import httplib2
except ImportError:
    from authy.contrib import httplib2


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
        http = httplib2.Http()
        http.follow_redirects = True

        params = {"api_key": self.api_key}
        body = ""

        if method == "GET":
            params.update(data)
        else:
            body = json.dumps(data)

        url = self.api_uri + path + "?"+urlencode(params)
        return http.request(url, method, headers=headers, body=body)

class Instance(object):
    def __init__(self, resource, response, content):
        self.resource = resource
        self.response = response

        try:
            self.content = json.loads(content)
        except ValueError:
            self.content = content

    def ok(self):
        return self.response['status'] == '200'

    def errors(self):
        if self.ok():
            return {}

        errors = self.content

        if(not isinstance(errors, dict)):
            errors = {"error": errors} # convert to dict for consistency
        elif('errors' in errors):
            errors = errors['errors']

        return errors

class User(Instance):
    def __init__(self, resource, response, content):
        super(User, self).__init__(resource, response, content)
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

        resp, content = self.post("/protected/json/users/new", data)

        return User(self, resp, content)

    def request_sms(self, user_id, options = {}):
        resp, content = self.get("/protected/json/sms/"+quote(str(user_id)), options)

        return Instance(self, resp, content)

class Token(Instance):
    pass

class Tokens(Resource):
    def verify(self, device_id, token, options = {}):
        if 'force' not in options:
            options['force'] = "true"
        resp, content = self.get("/protected/json/verify/"+quote(str(token))+"/"+quote(str(device_id)), options)
        return Token(self, resp, content)

class AppInfo(Instance):
    pass


class App(Resource):
    def details(self):
        resp, content = self.get("/protected/json/app/details")
        return AppInfo(self, resp, content)

    def stats(self):
        resp, content = self.get("/protected/json/app/stats")
        return AppInfo(self, resp, content)
