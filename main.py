from http.server import HTTPServer, BaseHTTPRequestHandler
from json import dumps

class MyRequestHandler(BaseHTTPRequestHandler):
    """
    GET requests handler
    """
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

def run():
    httpd = None
    try:
        server_address = ('127.0.0.1', 8000)
        httpd = HTTPServer(server_address, handler_factory)
        print('Server is listening')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Terminating connections')
        httpd.socket.close()
    except Exception as e:
        print('Error occurred:', e)
        httpd.socket.close()

if __name__ == '__main__':
    run()
