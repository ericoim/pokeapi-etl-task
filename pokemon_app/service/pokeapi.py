"""
PokeAPI Client Module

This module defines the external adapter for the PokeAPI service.
It handles HTTP communication, error handling, and data normalization
to convert external API responses into the application's internal data structure.
"""

from typing import Dict, Any, Optional
import requests
from requests.exceptions import RequestException

from pokemon_app.config import POKEAPI_BASE_URL
from pokemon_app.logger.logger import logger


class PokeAPIClient:
    """
    Adapter class for the external PokeAPI service.

    Responsibilities:
    - Fetching raw data via HTTP.
    - Handling connection errors and timeouts.
    - Normalizing external data formats (e.g., decimeters -> meters).
    """

    def __init__(self) -> None:
        """Initialize the client with configuration values."""
        self.base_url = POKEAPI_BASE_URL
        self._timeout = 10  # Timeout in seconds to prevent hanging

    def get_pokemon(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Fetches and processes Pokemon data from the external API.

        Args:
            name (str): The name of the Pokemon to fetch.

        Returns:
            Optional[Dict[str, Any]]: A dictionary of sanitized Pokemon data
            matching the internal model structure, or None if the request fails.
        """
        # API requires lowercase names
        target_url = f"{self.base_url}/pokemon/{name.lower()}"

        try:
            response = requests.get(target_url, timeout=self._timeout)
            response.raise_for_status()
            
            return self._process_pokemon_data(data=response.json())

        except RequestException as e:
            logger.error(f"Failed to fetch Pokemon '{name}' from API: {e}")
            return None

    def _process_pokemon_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitizes and formats the raw API response.

        Converts units (decimeters to meters, hectograms to kilograms)
        and flattens nested structures (abilities, stats, types, moves).

        Args:
            data (Dict[str, Any]): The raw JSON response from PokeAPI.

        Returns:
            Dict[str, Any]: The processed data ready for model instantiation.
        """
        return {
            'name': data['name'],
            # API returns height in decimeters, convert to meters
            'height': data['height'] / 10,
            # API returns weight in hectograms, convert to kilograms
            'weight': data['weight'] / 10,
            'base_experience': data['base_experience'],
            # Use .get() for lists to ensure empty list if key is missing
            'abilities': [item['ability']['name'] for item in data.get('abilities', [])],
            'stats': {
                item['stat']['name']: item['base_stat'] 
                for item in data.get('stats', [])
            },
            'types': [item['type']['name'] for item in data.get('types', [])],
            'moves': [item['move']['name'] for item in data.get('moves', [])]
        }
