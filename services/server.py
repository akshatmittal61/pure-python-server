import errno
from http.server import HTTPServer
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

def listen(handler_factory):
    while True:
        httpd = None
        try:
            print(f'Server is listening at {config.SERVER_ADDRESS}')
            httpd = HTTPServer(config.SERVER_ADDRESS, handler_factory)
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('Terminating connections')
            if httpd:
                httpd.socket.close()
                break
        except OSError as e:
            if e.errno == errno.EADDRINUSE:
                # get pid of process which is using it and print it
                pid = os.popen(f'lsof -ti tcp:{config.PORT}').read().strip()
                print(f'Current process: {os.getpid()} is trying to use port {config.PORT} but it is already in use by process with PID: {pid}')
                if httpd:
                    httpd.socket.close()
                find_and_terminate_process_using_port(config.PORT)
                sleep(1)
            else:
                raise e
        except Exception as e:
            print('Error occurred:', e)
            if httpd:
                httpd.socket.close()
                break
