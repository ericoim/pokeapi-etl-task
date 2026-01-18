"""
Pokemon Repository Layer

This module implements the Repository pattern for Pokemon data access.
It abstracts the underlying database interactions (SQLAlchemy sessions, queries)
providing a clean, object-oriented interface for the Service layer to use.
"""

from typing import Optional, List
from pokemon_app import db
from pokemon_app.model.pokemon import Pokemon


class PokemonRepository:
    """
    Handles all database persistence operations for Pokemon entities.
    """

    def get_by_name(self, name: str) -> Optional[Pokemon]:
        """
        Retrieves a Pokemon entity by its name (case-insensitive).

        Args:
            name (str): The name of the Pokemon to retrieve.

        Returns:
            Optional[Pokemon]: The Pokemon instance if found, otherwise None.
        """
        return Pokemon.query.filter_by(name=name.lower()).first()

    def get_all(self) -> List[Pokemon]:
        """
        Retrieves all Pokemon entities from the database.

        Returns:
            List[Pokemon]: A list of all stored Pokemon instances.
        """
        return Pokemon.query.all()

    def save(self, pokemon: Pokemon) -> Pokemon:
        """
        Persists a Pokemon entity to the database.
        Handles both creation (INSERT) and updates (UPDATE).

        Args:
            pokemon (Pokemon): The Pokemon entity to save.

        Returns:
            Pokemon: The saved Pokemon entity (refreshed with DB metadata like IDs).
        """
        db.session.add(pokemon)
        db.session.commit()
        return pokemon

    def delete(self, pokemon: Pokemon) -> None:
        """
        Removes a Pokemon entity from the database.

        Args:
            pokemon (Pokemon): The Pokemon entity to delete.
        """
        db.session.delete(pokemon)
        db.session.commit()
