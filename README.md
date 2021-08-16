# Docoin
Implementation of a cryptocurrency full node.

The code is fully tested and deployed using CircleCI and Heroku for continuous integration.

## Tech stack
- Python
- LevelDB
- Flask
- Heroku / CircleCI

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
