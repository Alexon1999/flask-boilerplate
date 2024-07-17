from flask import Flask
from .db import db
from .extensions import migrate, jwt, cors, ma, csrf
from .utils import (
    register_models,
    register_blueprints,
    configure_database,
)
from .logging import configure_logging
from .apps import INSTALLED_APPS


def create_app(name, config):
    app = Flask(name)
    app.config.from_object(config)

    # Directly initialize extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    cors.init_app(
        app, supports_credentials="true", resources={r"*": {"origins": "*"}}
    )
    csrf.init_app(app)

    register_models(INSTALLED_APPS)
    register_blueprints(app, INSTALLED_APPS)

    configure_database(app, db)

    configure_logging(app)

    return app
