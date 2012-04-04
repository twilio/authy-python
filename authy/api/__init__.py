import logging
import os
from authy import AuthyException
from authy.api.resources import Users
from authy.api.resources import Tokens

from urllib import urlencode
from urlparse import urljoin


class AuthyApiClient(object):
    """
    A client for accessing the Authy REST API
    """
    def __init__(self, api_key, api_uri="https://api.authy.com"):
        """
        Create a Authy REST API client.
        """
        self.api_uri = api_uri
        self.users = Users(api_uri, api_key)
        self.tokens = Tokens(api_uri, api_key)
        self.api_key = api_key
