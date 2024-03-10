from services.server import Server, Request, Response
from constants.tasks import tasks
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

def get_tasks(request: Request, response: Response) -> Response:
    return response.status(HTTPStatus.OK).data({
        'message': 'success',
        'data': tasks
    })

def get_task_by_id(request: Request, response: Response) -> Response:
    task_id = request.query_params.get('id')
    if not task_id:
        return response.status(HTTPStatus.BAD_REQUEST).data({
            'message': 'failure',
            'data': 'Task id is required'
        })
    task = list(filter(lambda t: t['id'] == int(task_id), tasks))
    if not task:
        return response.status(HTTPStatus.NOT_FOUND).data({
            'message': 'failure',
            'data': 'Task not found'
        })
    return response.status(HTTPStatus.OK).data({
        'message': 'success',
        'data': task[0]
    })

def add_task(request: Request, response: Response) -> Response:
    task = request.body
    if 'title' not in task or 'description' not in task:
        return response.status(HTTPStatus.BAD_REQUEST).data({
            'message': 'failure',
            'data': 'Both title and description are required'
        })
    task['id'] = len(tasks) + 1
    task['done'] = False
    tasks.append(task)
    return response.status(HTTPStatus.CREATED).data({
        'message': 'success',
        'data': task
    })

def update_task(request: Request, response: Response) -> Response:
    task_id = request.query_params.get('id')
    task = request.body
    if 'title' not in task and 'description' not in task and 'done' not in task:
        return response.status(HTTPStatus.BAD_REQUEST).data({
            'message': 'failure',
            'data': 'Either title, description or done is required'
        })
    task = list(filter(lambda t: t['id'] == int(task_id), tasks))
    if not task:
        return response.status(HTTPStatus.NOT_FOUND).data({
            'message': 'failure',
            'data': 'Task not found'
        })
    if 'title' in request.body:
        task[0]['title'] = request.body['title']
    if 'description' in request.body:
        task[0]['description'] = request.body['description']
    if 'done' in request.body:
        task[0]['done'] = request.body['done']
    return response.status(HTTPStatus.OK).data({
        'message': 'success',
        'data': tasks
    })

def delete_task(request: Request, response: Response) -> Response:
    task_id = request.query_params.get('id')
    task = list(filter(lambda t: t['id'] == int(task_id), tasks))
    if not task:
        return response.status(HTTPStatus.NOT_FOUND).data({
            'message': 'failure',
            'data': 'Task not found'
        })
    tasks.remove(task[0])
    return response.status(HTTPStatus.NO_CONTENT).data({
        'message': 'success',
        'data': tasks
    })

routes = [
    { 'method': 'GET', 'route': '/', 'handler': get_root },
    { 'method': 'GET', 'route': '/health', 'handler': get_health_api },
    { 'method': 'GET', 'route': '/tasks', 'handler': get_tasks },
    { 'method': 'GET', 'route': '/task', 'handler': get_task_by_id },
    { 'method': 'POST', 'route': '/task', 'handler': add_task },
    { 'method': 'PATCH', 'route': '/task', 'handler': update_task },
    { 'method': 'DELETE', 'route': '/task', 'handler': delete_task }
]

if __name__ == '__main__':
    app = Server(allowed_routes=routes)
    app.listen()
