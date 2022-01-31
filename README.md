
# Development setup
Dev setup requires Docker

## Build
```
docker-compose up --build
```

## Run
```
docker-compose up
```


# Connect to a PostgreSQL service from your local machine
@see https://docs.cloud.service.gov.uk/deploying_services/postgresql/#connect-to-a-postgresql-service-from-your-app

Run:
```
cf install-plugin conduit
```

```
cf conduit  postgres-13-dev
```





# Help Section
. venv/bin/activate

pip3 install Flask
pip3 freeze | grep Flask >> requirements.txt
pip3 freeze >> requirements.txt

pip list --format=freeze

pip3 freeze requirements.txt


## How to generate good secret keys
python -c 'import secrets; print(secrets.token_hex())'
