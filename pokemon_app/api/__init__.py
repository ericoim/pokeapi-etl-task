from flask import Blueprint

bp = Blueprint('api', __name__)

from pokemon_app.api import controller 