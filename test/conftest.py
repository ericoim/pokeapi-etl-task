"""
Pytest Configuration Module

This module defines fixtures for the test suite, including:
1. A Flask application instance configured for testing (In-Memory SQLite).
2. A test client for making HTTP requests.
3. A mock for the external PokeAPIClient to prevent real network calls.
"""

import pytest
from unittest.mock import MagicMock
from pokemon_app import create_app, db
from pokemon_app.config import Config

class TestConfig(Config):
    """Test configuration using in-memory SQLite."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # Disable CSRF protection in tests if enabled later
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    """
    Creates a fresh Flask application instance for each test.
    """
    app = create_app(TestConfig)
    
    with app.app_context():
        # Create all tables in the in-memory database
        db.create_all()
        yield app
        # Teardown: Drop all tables after test
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """
    Provides a test client for making requests to the application.
    """
    return app.test_client()

@pytest.fixture
def mock_pokeapi(mocker):
    """
    Mocks the PokeAPIClient to avoid real network requests.
    This patch ensures that any instance of PokeAPIClient used in the app
    will use our mock methods.
    """
    # Patch the class where it is IMPORTED in the controller/service
    # Since we instantiate it in the controller/service, we patch the class itself
    mock_get = mocker.patch('pokemon_app.service.pokeapi.PokeAPIClient.get_pokemon')
    return mock_get

@pytest.fixture
def sample_pokemon_data():
    """Returns a standardized Pokemon data dictionary for mocking."""
    return {
        'name': 'pikachu',
        'height': 0.4,
        'weight': 6.0,
        'base_experience': 112,
        'abilities': ['static'],
        'stats': {'speed': 90},
        'types': ['electric'],
        'moves': ['thunder-shock']
    }
