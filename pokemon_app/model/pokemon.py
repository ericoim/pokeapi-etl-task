"""
Pokemon Model Module

This module defines the database schema for the Pokemon entity using SQLAlchemy.
It maps the application's data structure to the underlying 'pokemon' database table
and handles serialization for API responses.
"""

from datetime import datetime
from typing import Dict, Any
from pokemon_app import db


class Pokemon(db.Model):
    """
    Pokemon model representing a Pokémon entity in the database.

    Attributes:
        id (int): Unique database primary key.
        name (str): The name of the Pokémon (unique constraint).
        height (float): Height in meters.
        weight (float): Weight in kilograms.
        base_experience (int): Base experience points yielded.
        abilities (List[str]): JSON list of ability names.
        stats (Dict[str, int]): JSON dictionary of stat names and values.
        types (List[str]): JSON list of elemental type names.
        moves (List[str]): JSON list of available move names.
        created_at (datetime): Timestamp when the record was created.
        updated_at (datetime): Timestamp when the record was last updated.
    """
    __tablename__ = 'pokemon'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Core Attributes
    name = db.Column(db.String(100), unique=True, nullable=False)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    base_experience = db.Column(db.Integer)

    # Complex Data Types (Stored as JSON)
    abilities = db.Column(db.JSON)
    stats = db.Column(db.JSON)
    types = db.Column(db.JSON)
    moves = db.Column(db.JSON)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Pokemon model instance to a dictionary.

        This helper method is essential for serializing the database model
        into a JSON-compatible format for API responses.

        Returns:
            Dict[str, Any]: A dictionary containing all Pokemon attributes
            with timestamps formatted as ISO strings.
        """
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height,
            'weight': self.weight,
            'base_experience': self.base_experience,
            'abilities': self.abilities,
            'stats': self.stats,
            'types': self.types,
            'moves': self.moves,
            # Ensure safe ISO formatting (though defaults prevent None, it is good practice)
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<Pokemon {self.name}>"
