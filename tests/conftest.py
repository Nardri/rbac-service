"""Module for Pytest Configuration"""

# system imports
from os import getenv, environ
import ctypes

# third party imports
import pytest
from sqlalchemy import event
from sqlalchemy.event.registry import _key_to_collection as collection

# local import
from app import create_app
from src.models.configs.database import database as db

TEST_ENV = 'testing'
environ['FLASK_ENV'] = TEST_ENV
ENV = getenv('FLASK_ENV')


@pytest.fixture(scope='session')
def flask_app():
    """Create a flask application instance for Pytest.
    Returns:
        Object: Flask application object
    """

    # create an application instance
    _app = create_app(ENV)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    # yield the application context for making requests
    yield _app

    ctx.pop()


@pytest.fixture
def client(flask_app):
    """Setup client for making http requests, this will be run on every
    test function.
    Args:
        flask_app (func): Flask application instance
    Returns:
        Object: flask application client instance
    """

    # initialize the flask test_client from the flask application instance
    client = flask_app.test_client()

    yield client


@pytest.fixture
def init_db():
    """Fixture to initialize the database"""

    db.create_all()
    yield db
    db.session.close()
    db.drop_all()


@pytest.fixture(scope='session')
def headers():
    """header data.
    Returns:
        dict: The header dictionary
    """

    return {'Content-Type': 'application/json', 'Authorization': 'Bearer iiu'}
