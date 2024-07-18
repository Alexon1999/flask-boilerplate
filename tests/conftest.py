import pytest
from configs import create_app


@pytest.fixture
def app():
    app = create_app(
        "testing",
        config={
            "TESTING": True,
            "SECRET_KEY": "test",
            "JWT_SECRET_KEY": "test_jwt_secret_key",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "OPENAPI_VERSION": "3.0.2",
        },
    )

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
