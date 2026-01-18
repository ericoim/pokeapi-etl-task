"""
Unit Tests for PokeAPIClient

Tests edge cases like network errors, timeouts, and 404s from the external provider.
"""
import pytest
import requests
from pokemon_app.service.pokeapi import PokeAPIClient

def test_client_fetch_success(mocker):
    """Test successful data fetching and normalization."""
    # Mock the requests.get call specifically
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        'name': 'bulbasaur',
        'height': 7,    # 7 decimeters
        'weight': 69,   # 69 hectograms
        'base_experience': 64,
        'abilities': [{'ability': {'name': 'overgrow'}}],
        'stats': [],
        'types': [],
        'moves': []
    }
    mock_response.raise_for_status.return_value = None
    
    mocker.patch('requests.get', return_value=mock_response)

    client = PokeAPIClient()
    result = client.get_pokemon('bulbasaur')

    # Verify conversions (Decimeters -> Meters, Hectograms -> KG)
    assert result['name'] == 'bulbasaur'
    assert result['height'] == 0.7  # 7 / 10
    assert result['weight'] == 6.9  # 69 / 10

def test_client_404_not_found(mocker):
    """Test API returning 404."""
    mock_response = mocker.Mock()
    # Simulate a 404 HTTPError
    error = requests.exceptions.HTTPError("404 Client Error")
    mock_response.raise_for_status.side_effect = error
    
    mocker.patch('requests.get', return_value=mock_response)

    client = PokeAPIClient()
    result = client.get_pokemon('missingno')

    assert result is None

def test_client_timeout(mocker):
    """Test API timeout."""
    # Simulate a Timeout exception
    mocker.patch('requests.get', side_effect=requests.exceptions.Timeout)

    client = PokeAPIClient()
    result = client.get_pokemon('snorlax')

    assert result is None
