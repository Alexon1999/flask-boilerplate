from flask import Flask
from flask.testing import FlaskCliRunner, FlaskClient
import pytest
from configs import create_app
from configs.settings import config_dict
from configs.db import db as _db


@pytest.fixture(scope="session")
def app() -> Flask:
    testing_config = config_dict["testing"]
    testing_config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    testing_config.JWT_SECRET = "test_jwt"
    testing_config.SECRET_KEY = "test"

    app = create_app(
        name="testing",
        config=testing_config,
    )

    with app.app_context():
        _db.create_all()

    return app


@pytest.fixture(scope="function")
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app) -> FlaskCliRunner:
    return app.test_cli_runner()
