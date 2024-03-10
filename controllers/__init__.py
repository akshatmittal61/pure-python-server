from services.server import Request, Response
from http import HTTPStatus

def get_root(request: Request, response: Response) -> Response:
    return response.status(HTTPStatus.OK).data({
        'message': 'success',
        'data': 'Hello World'
    })

def get_health_api(request, response: Response) -> Response:
    return response.status(HTTPStatus.OK).data({
        'message': 'success',
        'data': 'API is healthy'
    })
