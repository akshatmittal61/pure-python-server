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

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, allowed_routes = initial_routes, *args, **kwargs):
        self.allowed_routes = allowed_routes
        print('RequestHandler init', self.allowed_routes)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        current_route = self.path
        current_handler = None
        response = None
        if current_route in [routes[0] for routes in self.allowed_routes['GET']]:
            for route in self.allowed_routes['GET']:
                print('in loop', route)
                if route[0] == current_route:
                    current_handler = route[1]
                    break
        elif current_route in [routes[0] for routes in self.allowed_routes['POST']] or current_route in [routes[0] for routes in self.allowed_routes['PUT']] or current_route in [routes[0] for routes in self.allowed_routes['PATCH']] or current_route in [routes[0] for routes in self.allowed_routes['DELETE']]:
            self.send_response(405)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(dumps({ 'message': 'error', 'data': 'Method not allowed' }).encode('utf-8'))
            return
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(dumps({ 'message': 'error', 'data': 'Route not found' }).encode('utf-8'))
            return
        try:
            response = current_handler()
            print('response:', response)
            self.send_response(response['status'])
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(dumps(response['data']).encode('utf-8'))
        except Exception as e:
            print('Error occurred:', e)
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(dumps({ 'message': 'error', 'data': 'Internal Server Error' }).encode('utf-8'))


class Server:

    def __handler_factory__(self, *args, **kwargs):
        print(42, self.allowed_routes, *args, **kwargs)
        return RequestHandler(self.allowed_routes, *args, **kwargs)
    
    def __init__(self, allowed_routes=[]):
        self.httpd = None
        self.allowed_routes = initial_routes
        print(f'Original allowed_routes: {allowed_routes}')
        if allowed_routes:
            for route in allowed_routes:
                self.allowed_routes[route['method']].append((route['route'], route['handler']))
        print(f'allowed_routes: {self.allowed_routes}')
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
