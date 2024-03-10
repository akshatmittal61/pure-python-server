# Pure Python Server

A python server completely built with internal modules, without any external dependencies.

## Features

1. **In-built watcher**: Comprises in-built watcher which reloads the server on any file changes.
2. **Config Manager**: Has a built-in `ConfigManager` which loads all the OS variables and those mentioned in the `env` files right into memory as long as applications runs
3. **Request and Response**: Provides customized `Request` and `Response` for every API route to use efficiently with method chaining.

## Usage

Just clone the repository and start server with
```bash
./start.sh <development|staging|production>
```

### Environment Config

- For `development` environment variables, create a `.env.development` file and put variables in it.
- For `staging` environment variables, create a `.env.staging` file and put variables in it.
- For `production` environment variables, create a `.env.production` file and put variables in it.

### Priority order for environment variables

1. OS Environment Variables
2. `.env.development` or `.env.staging` or `.env.production` file (based on the environment)
3. `.env.local` file
4. `.env` file

## Author

[Akshat Mittal](https://akshatmittal61.vercel.app)
