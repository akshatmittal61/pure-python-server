from http.server import HTTPServer, BaseHTTPRequestHandler
from json import dumps
import os
import socket
import errno
from config import config
from services.server import Server

def get_root():
    return { 
        'status': 200,
        'data': {
            'message': 'Hello World'
        }
    }

def get_health_api():
    return { 
        'status': 200,
        'data': {
            'message': 'success',
            'data': 'Server health is good'
        }
    }

routes = [
    { 'method': 'GET', 'route': '/', 'handler': get_root },
    { 'method': 'GET', 'route': '/health', 'handler': get_health_api }
]

if __name__ == '__main__':
    app = Server(allowed_routes=routes)
    app.listen()
