import os

class ConfigManager:
    @staticmethod
    def load_env():
        environment = os.getenv('ENV') or 'development'
        print(f'Environment: {environment}')

        # Load environment variables from .env file(s)
        if environment == 'development':
            try:
                print('Loading .env.development file...')
                with open('.env.development') as f:
                    for line in f:
                        key, value = line.strip().split('=')
                        os.environ[key] = value
            except FileNotFoundError:
                print('No .env.development file found, loading .env.local file...')
                try:
                    with open('.env.local') as f:
                        for line in f:
                            key, value = line.strip().split('=')
                            os.environ[key] = value
                except FileNotFoundError:
                    print('No .env.local file found, loading .env file...')
                    try:
                        with open('.env') as f:
                            for line in f:
                                key, value = line.strip().split('=')
                                os.environ[key] = value
                    except FileNotFoundError:
                        print('No .env file found, skipping...')
                        pass
        elif environment == 'staging':
            try:
                print('Loading .env.staging file...')
                with open('.env.staging') as f:
                    for line in f:
                        key, value = line.strip().split('=')
                        os.environ[key] = value
            except FileNotFoundError:
                print('No .env.staging file found, loading .env.local file...')
                try:
                    with open('.env.local') as f:
                        for line in f:
                            key, value = line.strip().split('=')
                            os.environ[key] = value
                except FileNotFoundError:
                    print('No .env.local file found, loading .env file...')
                    try:
                        with open('.env') as f:
                            for line in f:
                                key, value = line.strip().split('=')
                                os.environ[key] = value
                    except FileNotFoundError:
                        print('No .env file found, skipping...')
                        pass
        elif environment == 'production':
            try:
                print('Loading .env.production file...')
                with open('.env.production') as f:
                    for line in f:
                        key, value = line.strip().split('=')
                        os.environ[key] = value
            except FileNotFoundError:
                print('No .env.production file found, loading .env.local file...')
                try:
                    with open('.env.local') as f:
                        for line in f:
                            key, value = line.strip().split('=')
                            os.environ[key] = value
                except FileNotFoundError:
                    print('No .env.local file found, loading .env file...')
                    try:
                        with open('.env') as f:
                            for line in f:
                                key, value = line.strip().split('=')
                                os.environ[key] = value
                    except FileNotFoundError:
                        print('No .env file found, skipping...')
                        pass
        else:
            try:
                print('Loading .env file...')
                with open('.env') as f:
                    for line in f:
                        key, value = line.strip().split('=')
                        os.environ[key] = value
            except FileNotFoundError:
                print('No .env file found, skipping...')
                pass

    def __init__(self):
        self.load_env()
        self.PORT = int(os.getenv('PORT') or '8000')
        self.SERVER_ADDRESS = ('127.0.0.1', self.PORT)
        self.ENV = os.getenv('ENV') or 'development'

    def get_all(self):
        env_file_variables = {key: self.get(key) for key in self.__dict__ if not key.startswith('_')}
        os_env_variables = {key: os.getenv(key) for key in os.environ}
        return {**env_file_variables, **os_env_variables}
        
    def get(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        elif key in os.environ:
            return os.environ[key]
        else:
            raise AttributeError(f"Attribute '{key}' not found")
        
    def set(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        elif key in os.environ:
            os.environ[key] = value
        else:
            raise AttributeError(f"Attribute '{key}' not found")

    def __iter__(self):
        return iter(self.__dict__.items())
    
    def __len__(self):
        return len(self.__dict__)
    
    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, value):
        self.set(key, value)

config = ConfigManager()
