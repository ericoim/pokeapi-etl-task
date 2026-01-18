"""
API Routes Module

This module defines the HTTP endpoints for the Pokémon Scouting Data Application.
It handles incoming requests, delegates business logic to the PokemonService,
and formats the responses (including proper HTTP status codes).
"""

from typing import Tuple
from flask import jsonify, Response
from pokemon_app.api import bp
from pokemon_app.service.pokemon_svc import PokemonService
from pokemon_app.service.pokeapi import PokeAPIClient
from pokemon_app.repository.pokemon_repo import PokemonRepository
from pokemon_app.config import POKEMON_LIST


def get_service() -> PokemonService:
    """
    Instantiates and returns the PokemonService with its dependencies.

    Returns:
        PokemonService: A configured service instance.
    """
    # Explicit dependency injection for clarity
    return PokemonService(
        repository=PokemonRepository(),
        api_client=PokeAPIClient()
    )


@bp.route('/pokemon', methods=['GET'])
def get_all_pokemon() -> Response:
    """
    Retrieves a list of all Pokémon stored in the database.

    Returns:
        Response: JSON list of Pokémon data.
    """
    service = get_service()
    return jsonify(service.get_all_pokemon())


@bp.route('/pokemon/<name>', methods=['GET'])
def get_pokemon(name: str) -> Tuple[Response, int]:
    """
    Retrieves details for a specific Pokémon by name.

    Args:
        name (str): The name of the Pokémon.

    Returns:
        Tuple[Response, int]: JSON Pokémon data or error message, with status code.
    """
    service = get_service()
    data = service.get_pokemon(name=name)

    if data:
        return jsonify(data), 200
    return jsonify({'error': 'Pokemon not found'}), 404


@bp.route('/pokemon/<name>', methods=['POST'])
def add_pokemon(name: str) -> Tuple[Response, int]:
    """
    Adds a new Pokémon to the database, fetching data from the external API.

    Args:
        name (str): The name of the Pokémon to add.

    Returns:
        Tuple[Response, int]: Success message and data (201/202) or error (404).
    """
    service = get_service()
    data, message = service.add_pokemon(name=name)

    if data:
        # 202 Accepted if it already exists, 201 Created if new
        status_code = 202 if "already exists" in message else 201
        return jsonify({'message': message, 'pokemon': data}), status_code

    return jsonify({'error': message}), 404


@bp.route('/pokemon/<name>', methods=['DELETE'])
def delete_pokemon(name: str) -> Tuple[Response, int]:
    """
    Removes a Pokémon from the database.

    Args:
        name (str): The name of the Pokémon to delete.

    Returns:
        Tuple[Response, int]: Success or error message with status code.
    """
    service = get_service()
    success = service.delete_pokemon(name=name)

    if success:
        return jsonify({'message': f'Successfully deleted {name}'}), 200
    return jsonify({'error': f'Pokemon {name} not found'}), 404


@bp.route('/pokemon/<name>', methods=['PUT', 'PATCH'])
def update_pokemon(name: str) -> Tuple[Response, int]:
    """
    Refreshes a specific Pokémon's data from the external API.

    Args:
        name (str): The name of the Pokémon to update.

    Returns:
        Tuple[Response, int]: Success or error message with status code.
    """
    service = get_service()
    success, message = service.update_pokemon(name=name)

    if success:
        return jsonify({'message': message}), 200
    return jsonify({'error': message}), 404


@bp.route('/refresh', methods=['POST'])
def refresh_data() -> Tuple[Response, int]:
    """
    Triggers a manual batch synchronization for all configured Pokémon.

    Returns:
        Tuple[Response, int]: Completion message with status code 200.
    """
    service = get_service()
    service.sync_config_list(pokemon_list=POKEMON_LIST)
    return jsonify({'message': 'Data refresh process completed'}), 200
