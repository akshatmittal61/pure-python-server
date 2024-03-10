import errno
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from config import config
from time import sleep
from typing import Callable
from server.response import Response
from server.request import Request
from server.router import Router
from server.utils import find_and_terminate_process_using_port
from server.constants import initial_routes

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, allowed_routes=None, *args, **kwargs):
        self.req = None
        self.res = None
        if allowed_routes is None:
            allowed_routes = initial_routes
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

    def __api_controller__(self, method, current_route) -> Callable[[Request, Response], Response] | None:
        current_controller = None
        if self.__is_method_allowed__(method, current_route):
            for route in self.allowed_routes[method]:
                if route[0] == current_route:
                    current_controller = route[1]
                    break
        return current_controller
    
    def __api_gateway__(self, method, route) -> Response:
        if self.__route_exists_but_method_not_allowed__(method, route):
            return self.res.status(405).data({ 'message': 'error', 'data': 'Method Not Allowed' }).send()
        else:
            return self.res.status(404).data({ 'message': 'error', 'data': 'Not Found' }).send()

    def do_GET(self):
        self.req = Request(self)
        self.res = Response(self)
        current_route = self.path.split('?')[0]
        controller = self.__api_controller__('GET', current_route)
        if controller is None:
            gateway_response = self.__api_gateway__('GET', current_route)
            return gateway_response
        try:
            result: Response = controller(self.req, self.res)
            return result.send()
        except Exception as e:
            print(f'Error occurred: {str(e)}')
            return self.res.status(500).data({ 'message': 'error', 'data': str(e) }).send()

    def do_POST(self):
        self.req = Request(self)
        self.res = Response(self)
        current_route = self.path.split('?')[0]
        controller = self.__api_controller__('POST', current_route)
        if controller is None:
            gateway_response = self.__api_gateway__('POST', current_route)
            return gateway_response
        try:
            result: Response = controller(self.req, self.res)
            return result.send()
        except Exception as e:
            print(f'Error occurred: {str(e)}')
            return self.res.status(500).data({ 'message': 'error', 'data': str(e) }).send()

    def do_PUT(self):
        self.req = Request(self)
        self.res = Response(self)
        current_route = self.path.split('?')[0]
        controller = self.__api_controller__('PUT', current_route)
        if controller is None:
            gateway_response = self.__api_gateway__('PUT', current_route)
            return gateway_response
        try:
            result: Response = controller(self.req, self.res)
            return result.send()
        except Exception as e:
            print(f'Error occurred: {str(e)}')
            return self.res.status(500).data({ 'message': 'error', 'data': str(e) }).send()

    def do_PATCH(self):
        self.req = Request(self)
        self.res = Response(self)
        current_route = self.path.split('?')[0]
        controller = self.__api_controller__('PATCH', current_route)
        if controller is None:
            gateway_response = self.__api_gateway__('PATCH', current_route)
            return gateway_response
        try:
            result: Response = controller(self.req, self.res)
            return result.send()
        except Exception as e:
            print(f'Error occurred: {str(e)}')
            return self.res.status(500).data({ 'message': 'error', 'data': str(e) }).send()

    def do_DELETE(self):
        self.req = Request(self)
        self.res = Response(self)
        current_route = self.path.split('?')[0]
        controller = self.__api_controller__('DELETE', current_route)
        if controller is None:
            gateway_response = self.__api_gateway__('DELETE', current_route)
            return gateway_response
        try:
            result: Response = controller(self.req, self.res)
            return result.send()
        except Exception as e:
            print(f'Error occurred: {str(e)}')
            return self.res.status(500).data({ 'message': 'error', 'data': str(e) }).send()

class Server:

    def __handler_factory__(self, *args, **kwargs):
        return RequestHandler(self.allowed_routes, *args, **kwargs)
    
    def __init__(self, router: Router):
        allowed_routes = router.get_routes()
        self.httpd = None
        self.allowed_routes = initial_routes
        if allowed_routes:
            for route in allowed_routes:
                self.allowed_routes[route['method']].append((route['route'], route['handler']))
        self.handler_factory = self.__handler_factory__

    def listen(self):
        while True:
            server_address = config.get('SERVER_ADDRESS')
            port = config.get('PORT')
            try:
                print(f'Server is listening at {server_address}')
                self.httpd = HTTPServer(config.get('SERVER_ADDRESS'), self.handler_factory)
                self.httpd.serve_forever()
            except KeyboardInterrupt:
                print('Terminating connections')
                if self.httpd:
                    self.httpd.socket.close()
                    break
            except OSError as e:
                if e.errno == errno.EADDRINUSE:
                    # get pid of process which is using it
                    pid = os.popen(f'lsof -ti tcp:{port}').read().strip()
                    print(f'Current process: {os.getpid()} is trying to use port {port} but it is already in use by process with PID: {pid}')
                    if self.httpd:
                        self.httpd.socket.close()
                    find_and_terminate_process_using_port(port)
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
