from authy import __version__
from authy.api.resources import Users
from authy.api.resources import Tokens
from authy.api.resources import Apps
from authy.api.resources import StatsResource
from authy.api.resources import Phones


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
        self.apps = Apps(api_uri, api_key)
        self.stats = StatsResource(api_uri, api_key)
        self.phones = Phones(api_uri, api_key)
        self.api_key = api_key

    def version(self):
        return __version__

