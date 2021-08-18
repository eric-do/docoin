# Docoin
Implementation of a cryptocurrency full node.

The code is fully tested and deployed using CircleCI and Heroku for continuous integration.

## Tech stack
- Server: Python / Flask
- Database: Postgres for tracking UTXO
- Deployment: Heroku  / CircleCI

## Server
A local instance of the server can be ran with
```
gunicorn app:app
```

## Tests
Tests are implemented with pytest and can be ran with
```
pytest
```

## Database
UTXO are tracked with Postgres. Seeding script can be used to generate large amounts of fake data to test query performance.

Since we frequently

## Virtual environment
Start the virtual environment with
```
source .venv/bin/activate
```