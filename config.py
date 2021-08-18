from os import environ, path
from dotenv import load_dotenv

# Load variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# Database config
DATABASE_NAME = environ.get('DATABASE_NAME')
DATABASE_USERNAME = environ.get('DATABASE_USERNAME')