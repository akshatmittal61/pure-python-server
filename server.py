from http.server import HTTPServer, BaseHTTPRequestHandler
from json import dumps
import os
import socket
import errno
from config import config
from services.server import Server, Request, Response

def get_root(request: Request, response: Response) -> Response:
    print(request)
    return response.status(200).data({
        'message': 'success',
        'data': 'Hello World'
    })

def get_health_api(request, response: Response) -> Response:
    return response.status(200).data({
        'message': 'success',
        'data': 'API is healthy'
    })

routes = [
    { 'method': 'GET', 'route': '/', 'handler': get_root },
    { 'method': 'GET', 'route': '/health', 'handler': get_health_api },
    { 'method': 'POST', 'route': '/12', 'handler': get_health_api },
]

if __name__ == '__main__':
    app = Server(allowed_routes=routes)
    app.listen()
