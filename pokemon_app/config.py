"""
Application Configuration Module

This module defines the configuration settings for the Flask application,
including database connections, external API endpoints, and business data constants.
"""

from pathlib import Path
from typing import List

# Resolve the project root directory
# config.py is in pokemon_app/, so parent -> pokemon_app, parent.parent -> root
BASE_DIR = Path(__file__).resolve().parent.parent

# Database Connection URI
DATABASE_URL = f"sqlite:///{BASE_DIR}/pokemon.db"

# External PokeAPI Base URL
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"

# Initial list of Pokemon to scout (as requested in the Project Brief).
# Note: The Service layer handles typo correction form the docs (e.g., 'terodactyl' -> 'aerodactyl').
POKEMON_LIST: List[str] = [
    "pikachu",
    "dhelmise",
    "charizard",
    "parasect",
    "terodactyl",  # The service layer will automatically map this to 'aerodactyl'
    "kingler"
]


class Config:
    """
    Flask Application Configuration Class.
    """
    SQLALCHEMY_DATABASE_URI: str = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
