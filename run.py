"""
Application Entry Point

This module serves as the entry point for the Flask application.
It handles the application factory creation, performs an initial data synchronization
on startup, and launches the development server.
"""

from pokemon_app import create_app
from pokemon_app.config import POKEMON_LIST
from pokemon_app.service.pokemon_svc import PokemonService
from pokemon_app.repository.pokemon_repo import PokemonRepository
from pokemon_app.service.pokeapi import PokeAPIClient

# Initialize the Flask application using the factory pattern
app = create_app()


def initial_sync() -> None:
    """
    Performs the initial synchronization of Pokemon data.

    This helper function sets up the necessary service dependencies
    and triggers the batch processing of the configured Pokemon list.
    It is intended to be run within the application context before the server starts.
    """
    # Manual dependency injection for the startup script
    repository = PokemonRepository()
    api_client = PokeAPIClient()
    service = PokemonService(repository=repository, api_client=api_client)

    service.sync_config_list(pokemon_list=POKEMON_LIST)


if __name__ == '__main__':
    # Ensure database tables exist and initial data is populated
    with app.app_context():
        initial_sync()

    # Launch the Flask development server
    app.run(debug=True)
