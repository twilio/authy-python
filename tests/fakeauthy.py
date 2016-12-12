

import json

from threading import Thread

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer


class AuthyAPIHandler(BaseHTTPRequestHandler):

    requests = []
    responses = []

    default_response = ({}, 200, None)

    def do_GET(self):

        content_len = int(self.headers.getheader('content-length', 0))
        content = self.rfile.read(content_len)

        self.requests.append((self.path, content))

        try:
            response, status_code, headers = self.responses.pop(0)
        except IndexError:
            response, status_code, headers = self.default_response

        self.send_response(status_code)

        headers = headers or {'Content-Type': 'application/json'}
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()

        self.wfile.write(json.dumps(response))
        self.finish()

    do_POST = do_GET


class FakeAuthyAPIServer(object):

    def __init__(self, port, host='localhost'):

        self.host = host
        self.port = port
        self.server = None
        self.thread = None

    def set_response(self, response, code=200, headers=None):

        AuthyAPIHandler.responses.append((response, code, headers))

    def reset(self):

        AuthyAPIHandler.requests = []
        AuthyAPIHandler.responses = []

    def start(self):

        self.server = HTTPServer((self.host, self.port), AuthyAPIHandler)
        self.thread = Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):

        self.reset()
        self.server.shutdown()
        self.server.socket.close()
        self.thread = None


if __name__ == '__main__':

    import requests

    fake_authy_api = FakeAuthyAPIServer(port=12345, host='0.0.0.0')

    try:
        fake_authy_api.start()
        fake_authy_api.set_response({'message': 'Not Found'}, code=404)

        response = requests.get('http://localhost:12345/protected/json/phones/info',
                                headers={'Header': 'value'})
        print(response.status_code)
        print(response.text)

        resp = requests.get('http://localhost:12345/protected/json/phones/info',
                            headers={'Header': 'value'})
        print(response.status_code)
        print(response.text)
    finally:
        fake_authy_api.stop()


# EOF
