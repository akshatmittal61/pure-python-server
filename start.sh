if [ -z "$1" ]; then
  echo "Usage: start.sh <development|staging|production>"
  exit 1
fi

case $1 in
  development)
    echo "Setting ENV to development"
    export ENV=development
    if [ -f .env.development ]; then
      echo "Loading .env.development"
      export $(cat .env.development | xargs)
    elif [ -f .env.local ]; then
      echo ".env.development not found, loading .env.local"
      export $(cat .env.local | xargs)
    elif [ -f .env ]; then
      echo ".env.development and .env.local not found, loading .env"
      export $(cat .env | xargs)
    fi
    ;;
  staging)
    echo "Setting ENV to staging"
    export ENV=staging
    if [ -f .env.staging ]; then
      echo "Loading .env.staging"
      export $(cat .env.staging | xargs)
    elif [ -f .env.local ]; then
      echo ".env.staging not found, loading .env.local"
      export $(cat .env.local | xargs)
    elif [ -f .env ]; then
      echo ".env.staging and .env.local not found, loading .env"
      export $(cat .env | xargs)
    fi
    ;;
  production)
    echo "Setting ENV to production"
    export ENV=production
    if [ -f .env.production ]; then
      echo "Loading .env.production"
      export $(cat .env.production | xargs)
    elif [ -f .env.local ]; then
      echo ".env.production not found, loading .env.local"
      export $(cat .env.local | xargs)
    elif [ -f .env ]; then
      echo ".env.production and .env.local not found, loading .env"
      export $(cat .env | xargs)
    fi
    ;;
  *)
    echo "Usage: start.sh <development|staging|production>"
    exit 1
    ;;
esac

# Start the server
python3 main.py
