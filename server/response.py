from json import dumps
from typing import Self

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
