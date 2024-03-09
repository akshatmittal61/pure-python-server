from http.server import HTTPServer, BaseHTTPRequestHandler
from json import dumps
import os
import socket
import errno
from config import config
from services.server import listen

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response_data = { 'message': 'success', 'data': 'Server health is good' }
        response_json = dumps(response_data)
        self.wfile.write(response_json.encode('utf-8'))
        return self

def handler_factory(*args):
    return MyRequestHandler(*args)


if __name__ == '__main__':
    listen(handler_factory=handler_factory)
