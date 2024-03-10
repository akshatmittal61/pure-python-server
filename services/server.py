import errno
from http.server import HTTPServer, BaseHTTPRequestHandler
from json import dumps
import os
import socket
from config import config
from time import sleep
from typing import Self

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

class Response:
    def __init__(self, request_handler) -> None:
        self.status_code = 200
        self.response_data = {}
        self.content_type = 'application/json'
        self.request_handler = request_handler

    def status(self, status_code: int) -> Self:
        self.status_code = status_code
        return self

    def data(self, data: dict) -> Self:
        self.response_data = data
        return self

    def content_type(self, content_type: str) -> Self:
        self.content_type = content_type
        return self

    def build(self) -> dict:
        return {
            'status': self.status_code,
            'response_data': self.response_data,
            'content_type': self.content_type
        }

    def send(self) -> Self:
        self.request_handler.send_response(self.status_code)
        self.request_handler.send_header('Content-type', self.content_type)
        self.request_handler.end_headers()
        self.request_handler.wfile.write(dumps(self.response_data).encode('utf-8'))
        return self

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, allowed_routes = initial_routes, *args, **kwargs):
        self.allowed_routes = allowed_routes
        self.response = Response(self)
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

    def __api_controller__(self, method, current_route) -> Response | None:
        current_controller = None
        if self.__is_method_allowed__(method, current_route):
            for route in self.allowed_routes[method]:
                if route[0] == current_route:
                    current_controller = route[1]
                    break
        return current_controller
    
    def __api_gateway__(self, method, route) -> Response:
        if self.__route_exists_but_method_not_allowed__(method, route):
            return self.response.status(405).data({ 'message': 'error', 'data': 'Method Not Allowed' }).send()
        else:
            return self.response.status(404).data({ 'message': 'error', 'data': 'Not Found' }).send()

    def do_GET(self):
        current_route = self.path
        controller = self.__api_controller__('GET', current_route)
        if controller is None:
            gateway_response = self.__api_gateway__('GET', current_route)
            return gateway_response
        try:
            result: Response = controller({}, self.response)
            return result.send()
        except Exception as e:
            print(f'Error occurred: {str(e)}')
            return self.response.status(500).data({ 'message': 'error', 'data': str(e) }).send()


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
