import errno
from http.server import HTTPServer, BaseHTTPRequestHandler
from json import dumps
import os
import socket
from config import config
from time import sleep

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def find_and_terminate_process_using_port(port):
    if is_port_in_use(port):
        if os.name == 'posix':  # For Unix-like systems (Linux, MacOS)
            os.system(f'lsof -ti tcp:{port} | xargs -r kill -9')
        elif os.name == 'nt':  # For Windows
            os.system(f'netstat -ano | findstr :{port} | findstr LISTENING | '
                  'awk "{print $5}" | xargs taskkill /F /PID')
        else:
            raise NotImplementedError(f"Unsupported OS: {os.name}")
        
initial_routes = {
    'GET': [],
    'POST': [],
    'PUT': [],
    'PATCH': [],
    'DELETE': []
}

allowed_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, allowed_routes = initial_routes, *args, **kwargs):
        self.allowed_routes = allowed_routes
        super().__init__(*args, **kwargs)

    def __is_method_allowed__(self, method, current_route):
        return current_route in [routes[0] for routes in self.allowed_routes[method]]
    
    def __is_route_allowed__(self, current_route):
        return (
            self.__is_method_allowed__('GET', current_route) or
            self.__is_method_allowed__('POST', current_route) or
            self.__is_method_allowed__('PUT', current_route) or
            self.__is_method_allowed__('PATCH', current_route) or
            self.__is_method_allowed__('DELETE', current_route)
        )
    
    def __route_exists_but_method_not_allowed__(self, method, current_route):
        is_route_allowed = self.__is_route_allowed__(current_route)
        is_method_allowed = self.__is_method_allowed__(method, current_route)
        return is_route_allowed and not is_method_allowed
    
    def __response__(self, status, data, content_type = 'application/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(dumps(data).encode('utf-8'))

    def __api_handler__(self, method, current_route):
        current_handler = None
        if self.__is_method_allowed__(method, current_route):
            for route in self.allowed_routes[method]:
                if route[0] == current_route:
                    current_handler = route[1]
                    break
        return current_handler

    def do_GET(self):
        current_route = self.path
        response = None
        current_handler = self.__api_handler__('GET', current_route)
        if current_handler is not None:
            try:
                response = current_handler()
                self.__response__(response['status'], response['data'])
            except Exception as e:
                print('Error occurred:', e)
                self.__response__(500, { 'message': 'error', 'data': 'Internal Server Error' })
        else:
            if self.__route_exists_but_method_not_allowed__('GET', current_route):
                self.__response__(405, { 'message': 'error', 'data': 'Method Not Allowed' })
            else:
                self.__response__(404, { 'message': 'error', 'data': 'Not Found' })


class Server:

    def __handler_factory__(self, *args, **kwargs):
        return RequestHandler(self.allowed_routes, *args, **kwargs)
    
    def __init__(self, allowed_routes=[]):
        self.httpd = None
        self.allowed_routes = initial_routes
        if allowed_routes:
            for route in allowed_routes:
                self.allowed_routes[route['method']].append((route['route'], route['handler']))
        self.handler_factory = self.__handler_factory__

    def listen(self):
        while True:
            try:
                print(f'Server is listening at {config.SERVER_ADDRESS}')
                self.httpd = HTTPServer(config.SERVER_ADDRESS, self.handler_factory)
                self.httpd.serve_forever()
            except KeyboardInterrupt:
                print('Terminating connections')
                if self.httpd:
                    self.httpd.socket.close()
                    break
            except OSError as e:
                if e.errno == errno.EADDRINUSE:
                    # get pid of process which is using it and print it
                    pid = os.popen(f'lsof -ti tcp:{config.PORT}').read().strip()
                    print(f'Current process: {os.getpid()} is trying to use port {config.PORT} but it is already in use by process with PID: {pid}')
                    if self.httpd:
                        self.httpd.socket.close()
                    find_and_terminate_process_using_port(config.PORT)
                    sleep(1)
                else:
                    raise e
            except Exception as e:
                print('Error occurred:', e)
                if self.httpd:
                    self.httpd.socket.close()
                    break

    def start(self):
        self.listen()
