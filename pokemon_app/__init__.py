from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pokemon_app.config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from pokemon_app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    with app.app_context():
        db.create_all()

    return app 