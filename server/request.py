from json import loads

class Request:
    def __init__(self, request_handler) -> None:
        self.request_handler = request_handler
        self.data = {}
        self.query_params = {}
        self.body = {}
        self.headers = {}
        self.method = ''
        self.path = ''
        self.request_version = ''
        self.__parse_request__(request_handler)

    def __parse_query_params__(self, query_params):
        self.query_params = dict([param.split('=') for param in query_params.split('&')])

    def __parse_body__(self):
        content_length = int(self.headers['Content-Length'])
        if content_length:
            body_data = self.request_handler.rfile.read(content_length).decode('utf-8')
            parsed_body = loads(body_data)
            self.body = parsed_body

    def __parse_headers__(self, headers):
        self.headers = headers

    def __parse_request__(self, request):
        self.__parse_headers__(self.request_handler.headers)
        if request:
            self.method = request.requestline.split(' ')[0]
            self.path = request.requestline.split(' ')[1]
            self.request_version = request.requestline.split(' ')[2]
            if '?' in self.path:
                self.path, query_params = self.path.split('?')
                self.__parse_query_params__(query_params)
            if self.method in ['POST', 'PUT', 'PATCH']:
                self.__parse_body__()

    def build(self):
        return {
            'method': self.method,
            'path': self.path,
            'query_params': self.query_params,
            'body': self.body,
            'headers': self.headers,
            'request_version': self.request_version
        }

    def parse(self):
        self.__parse_request__(self.request_handler.requestline)
        return self

    def get(self, key):
        return self.query_params[key] if key in self.query_params else None
