# Pure Python Server

A python server completely built with internal modules, without any external dependencies.

## Features

1. **In-built watcher**: Comprises in-built watcher which reloads the server on any file changes.
2. **Config Manager**: Has a built-in `ConfigManager` which loads all the OS variables and those mentioned in the `.env` files right into memory as long as applications runs
3. **Request and Response**: Provides customized `Request` and `Response` for every API route to use efficiently with method chaining.

## Usage

Just clone the repository and start server with
```bash
python3 main.py
```

### Environment Config

- For `development` environment variables, create a `.env.local` file and put variables in it.
- For `production` environment variables, create a `.env.production` file and put variables in it.

## Author

[Akshat Mittal](https://akshatmittal61.vercel.app)
