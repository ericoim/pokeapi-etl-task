"""
Integration Tests for Pokemon API

These tests verify the full pipeline: Controller -> Service -> Repository -> Database.
We mock ONLY the external API response.
"""

def test_add_pokemon_happy_path(client, mock_pokeapi, sample_pokemon_data):
    """
    Test adding a new Pokemon (Pikachu).
    Should return 201 Created and store data in DB.
    """
    # Setup Mock
    mock_pokeapi.return_value = sample_pokemon_data

    # Execute
    response = client.post('/api/v1/pokemon/pikachu')
    
    # Assert HTTP Response
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['pokemon']['name'] == 'pikachu'
    assert json_data['message'] == 'Successfully added pikachu to database'

    # Assert Persistence (Fetch it back)
    get_response = client.get('/api/v1/pokemon/pikachu')
    assert get_response.status_code == 200

def test_business_logic_typo_correction(client, mock_pokeapi):
    """
    Test the 'Terodactyl' business rule.
    Input: 'terodactyl'
    Expected Behavior: Service fetches and stores 'aerodactyl'.
    """
    # Setup Mock to expect 'aerodactyl' (normalized name), NOT 'terodactyl'
    aerodactyl_data = {'name': 'aerodactyl', 'height': 1.8, 'weight': 59.0}
    mock_pokeapi.return_value = aerodactyl_data

    # Execute with TYPO
    response = client.post('/api/v1/pokemon/terodactyl')

    # Assertions
    assert response.status_code == 201
    assert response.get_json()['pokemon']['name'] == 'aerodactyl'
    
    # Verify the mock was called with the CORRECTED name
    mock_pokeapi.assert_called_with('aerodactyl')

def test_idempotency_add_twice(client, mock_pokeapi, sample_pokemon_data):
    """
    Test adding the same Pokemon twice.
    First time: 201 Created.
    Second time: 202 Accepted (already exists).
    """
    mock_pokeapi.return_value = sample_pokemon_data

    # First Add
    client.post('/api/v1/pokemon/pikachu')
    
    # Second Add
    response = client.post('/api/v1/pokemon/pikachu')
    
    assert response.status_code == 202
    assert "already exists" in response.get_json()['message']
    # Mock should likely only be called once if we check DB first, 
    # but depending on implementation, ensuring DB state is key.

def test_get_nonexistent_pokemon(client):
    """Test getting a Pokemon that hasn't been added yet."""
    response = client.get('/api/v1/pokemon/mewtwo')
    assert response.status_code == 404
    assert 'error' in response.get_json()

def test_delete_pokemon(client, mock_pokeapi, sample_pokemon_data):
    """Test the deletion workflow."""
    mock_pokeapi.return_value = sample_pokemon_data
    
    # Add first
    client.post('/api/v1/pokemon/pikachu')
    
    # Delete
    del_response = client.delete('/api/v1/pokemon/pikachu')
    assert del_response.status_code == 200
    
    # Verify it's gone
    get_response = client.get('/api/v1/pokemon/pikachu')
    assert get_response.status_code == 404
