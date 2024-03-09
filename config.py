import os

class ConfigManager:
    def load_env(self):
        with open('.env') as f:
            for line in f:
                key, value = line.strip().split('=')
                os.environ[key] = value

    def __init__(self):
        self.load_env()
        self.PORT = int(os.getenv('PORT')) or 8000
        self.SERVER_ADDRESS = ('127.0.0.1', self.PORT)
        
    def get(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise AttributeError(f"Attribute '{key}' not found")
        
    def set(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise AttributeError(f"Attribute '{key}' not found")
        
    def __str__(self):
        return f"PORT: {self.PORT}, SERVER_ADDRESS: {self.SERVER_ADDRESS}"
    
    def __repr__(self):
        return f"ConfigManager(PORT: {self.PORT}, SERVER_ADDRESS: {self.SERVER_ADDRESS})"
    
    def __iter__(self):
        return iter(self.__dict__.items())
    
    def __len__(self):
        return len(self.__dict__)
    
    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, value):
        self.set(key, value)

config = ConfigManager()
