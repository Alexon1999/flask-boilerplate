from flask import Flask
from configs.db import db
from configs.extensions import migrate, jwt
from importlib import import_module


def create_app(name, config):
    app = Flask(name)
    app.config.from_object(config)

    # Directly initialize extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    register_blueprints(app, config.INSTALLED_APPS)
    return app


def register_blueprints(app, apps_list):
    for module_name in apps_list:
        module = import_module("{}.routes".format(module_name))
        app.register_blueprint(module.blueprint)
