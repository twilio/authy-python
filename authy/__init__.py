__version__ = '2.2.1'


class AuthyException(Exception):
    pass

class AuthyFormatException(AuthyException):
	pass

class AuthyApiException(AuthyException):

    def __init__(self, status, uri, msg=""):
        self.uri = uri
        self.status = status
        self.msg = msg

    def __str__(self):
        return "HTTP ERROR %s: %s \n %s" % (self.status, self.msg, self.uri)
