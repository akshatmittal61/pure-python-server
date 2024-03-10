from server import Server
from controllers import get_root, get_health_api
from controllers.tasks import get_tasks, get_task_by_id, add_task, update_task, delete_task

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
