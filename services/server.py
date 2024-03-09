import errno
from http.server import HTTPServer
import os
import socket
from config import config

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

def listen(handler_factory):
    httpd = None
    try:
        print('Server is listening')
        httpd = HTTPServer(config.SERVER_ADDRESS, handler_factory)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Terminating connections')
        if httpd:
            httpd.socket.close()
    except OSError as e:
        if e.errno == errno.EADDRINUSE:
            print('Address already in use, terminating process...')
            find_and_terminate_process_using_port(8000)
            listen(handler_factory)
        else:
            raise e
    except Exception as e:
        print('Error occurred:', e)
        if httpd:
            httpd.socket.close()
            listen(handler_factory)
