from http.server import HTTPServer, BaseHTTPRequestHandler
from json import dumps
import os
import socket
import errno

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

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def find_and_terminate_process_using_port(port):
    if is_port_in_use(8000):
        if os.name == 'posix':  # For Unix-like systems (Linux)
            os.system(f'lsof -ti tcp:{port} | xargs -r kill -9')
        elif os.name == 'nt':  # For Windows
            os.system(f'netstat -ano | findstr :{port} | findstr LISTENING | '
                  'awk "{print $5}" | xargs taskkill /F /PID')
        else:
            raise NotImplementedError(f"Unsupported OS: {os.name}")

def run():
    httpd = None
    try:
        print('Server is listening')
        server_address = ('127.0.0.1', 8000)
        httpd = HTTPServer(server_address, handler_factory)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Terminating connections')
        if httpd:
            httpd.socket.close()
    except OSError as e:
        if e.errno == errno.EADDRINUSE:
            print('Address already in use, terminating process...')
            find_and_terminate_process_using_port(8000)
            run()
        else:
            raise e
    except Exception as e:
        print('Error occurred:', e)
        if httpd:
            httpd.socket.close()
            run()

if __name__ == '__main__':
    run()
