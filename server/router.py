class Router:
    def __init__(self):
        self.routes = []

    def get(self, path, callback):
        self.routes.append({ 'method': 'GET', 'route': path, 'handler': callback })

    def post(self, path, callback):
        self.routes.append({ 'method': 'POST', 'route': path, 'handler': callback })

    def patch(self, path, callback):
        self.routes.append({ 'method': 'PATCH', 'route': path, 'handler': callback })

    def delete(self, path, callback):
        self.routes.append({ 'method': 'DELETE', 'route': path, 'handler': callback })

    def get_routes(self):
        return self.routes
