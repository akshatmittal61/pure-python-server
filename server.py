from server import Server
from routes import router

if __name__ == '__main__':
    app = Server(router)
    app.listen()
