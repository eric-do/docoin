import tempfile
import pytest

from docoin import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app({"TESTING": True, "DATABASE": db_path})

    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
