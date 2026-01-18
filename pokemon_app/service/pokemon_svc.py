"""
Pokemon Service Layer

This module implements the core business logic for the application.
It orchestrates the flow of data between the external PokeAPI client,
the internal database repository, and the application controllers.

Key Responsibilities:
- Input sanitization and normalization (handling business-specific typos).
- Idempotency checks (preventing duplicate data).
- Coordination of data fetching and persistence.
"""

from typing import Optional, List, Dict, Any, Tuple
from pokemon_app.model.pokemon import Pokemon
from pokemon_app.service.pokeapi import PokeAPIClient
from pokemon_app.repository.pokemon_repo import PokemonRepository
from pokemon_app.logger.logger import logger


class PokemonService:
    """
    Service class handling the business logic for Pokemon data operations.
    """

    def __init__(self, repository: PokemonRepository, api_client: PokeAPIClient) -> None:
        """
        Initialize the service with necessary dependencies.

        Args:
            repository (PokemonRepository): Data access layer for persistence.
            api_client (PokeAPIClient): External client for fetching Pokemon data.
        """
        self.repository = repository
        self.api_client = api_client
        # Business Logic: Mappings to correct known typos in input data
        # Example: "Terodactyl" (Brief) -> "Aerodactyl" (Actual API Name)
        self._name_mapping = {
            "terodactyl": "aerodactyl"
        }

    def _normalize_name(self, name: str) -> str:
        """
        Sanitizes and corrects Pokemon names based on business rules.

        Args:
            name (str): The raw input name.

        Returns:
            str: The sanitized and mapped name (lowercase).
        """
        clean_name = name.lower().strip()
        return self._name_mapping.get(clean_name, clean_name)

    def get_all_pokemon(self) -> List[Dict[str, Any]]:
        """
        Retrieve all Pokemon stored in the local database.

        Returns:
            List[Dict[str, Any]]: A list of serialized Pokemon data dictionaries.
        """
        return [p.to_dict() for p in self.repository.get_all()]

    def get_pokemon(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific Pokemon from the local database.

        Args:
            name (str): The name of the Pokemon to retrieve.

        Returns:
            Optional[Dict[str, Any]]: Serialized Pokemon data if found, else None.
        """
        normalized_name = self._normalize_name(name)
        pokemon = self.repository.get_by_name(normalized_name)
        return pokemon.to_dict() if pokemon else None

    def add_pokemon(self, name: str) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Fetches a Pokemon from the external API and persists it to the database.
        Enforces idempotency by checking if the record already exists.

        Args:
            name (str): The name of the Pokemon to add.

        Returns:
            Tuple[Optional[Dict[str, Any]], str]: A tuple containing the
            serialized Pokemon data (if successful) and a status message.
        """
        normalized_name = self._normalize_name(name)

        # 1. Check local DB first to enforce idempotency
        existing = self.repository.get_by_name(normalized_name)
        if existing:
            return existing.to_dict(), f"Pokemon {normalized_name} already exists in database"

        # 2. Fetch from External Source
        raw_data = self.api_client.get_pokemon(normalized_name)
        if not raw_data:
            # We use the original name in the error message to help the user debug their input
            return None, f"Failed to fetch data for {name} (mapped to {normalized_name})"

        # 3. Create and Save
        # Note: raw_data keys must match the Pokemon model columns.
        new_pokemon = Pokemon(**raw_data)
        self.repository.save(new_pokemon)

        return new_pokemon.to_dict(), f"Successfully added {normalized_name} to database"

    def delete_pokemon(self, name: str) -> bool:
        """
        Deletes a Pokemon from the local database.

        Args:
            name (str): The name of the Pokemon to delete.

        Returns:
            bool: True if deletion was successful, False if the record was not found.
        """
        normalized_name = self._normalize_name(name)
        pokemon = self.repository.get_by_name(normalized_name)

        if pokemon:
            self.repository.delete(pokemon)
            return True
        return False

    def update_pokemon(self, name: str) -> Tuple[bool, str]:
        """
        Refreshes an existing Pokemon's data by re-fetching from the API.

        Args:
            name (str): The name of the Pokemon to update.

        Returns:
            Tuple[bool, str]: A tuple containing the success status and a message.
        """
        normalized_name = self._normalize_name(name)
        pokemon = self.repository.get_by_name(normalized_name)

        if not pokemon:
            return False, f"Pokemon {normalized_name} not found locally"

        raw_data = self.api_client.get_pokemon(normalized_name)
        if not raw_data:
            return False, f"Failed to fetch update for {normalized_name}"

        # Update fields dynamically
        for key, value in raw_data.items():
            if hasattr(pokemon, key):
                setattr(pokemon, key, value)

        self.repository.save(pokemon)
        return True, f"Successfully updated {normalized_name}"

    def sync_config_list(self, pokemon_list: List[str]) -> None:
        """
        Batch process to synchronize the configured list of Pokemon on startup.

        Args:
            pokemon_list (List[str]): List of Pokemon names to sync.
        """
        logger.info("Starting batch sync...")
        for name in pokemon_list:
            data, msg = self.add_pokemon(name)
            if data and "already exists" not in msg:
                logger.info(msg)
            elif "already exists" in msg:
                logger.info(f"Skipping {name}: {msg}")
            else:
                logger.error(msg)
        logger.info("Batch sync finished.")
