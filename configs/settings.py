import os
import datetime
import environ

env = environ.Env()


class Config(object):
    # i want parent of parent directory path of the current file
    _file_path = os.path.abspath(__file__)
    base_dir = os.path.dirname(os.path.dirname(_file_path))

    APP_NAME = env("APP_NAME", default="FlaskAPP")
    SECRET_KEY = env("SECRET_KEY")
    PROPAGATE_EXCEPTIONS = True
    DEBUG = env.bool("DEBUG", default=False)

    # Configuration of Flask-JWT-Extended
    JWT_SECRET_KEY = env("JWT_SECRET_KEY")
    # Determines the minutes that the access token remains active
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=30)
    # Determines the days that the refresh token remains active
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
    # Algorithm used to generate the token
    JWT_ALGORITHM = "HS256"
    # Algorithm used to decode the token
    JWT_DECODE_ALGORITHMS = "HS256"
    # Header that should contain the JWT in a request
    JWT_HEADER_NAME = "Authorization"
    # Word that goes before the token in the Authorization header in this case empty
    JWT_HEADER_TYPE = "Bearer"
    # Where to look for a JWT when processing a request.
    JWT_TOKEN_LOCATION = "headers"

    # Config API documents
    API_TITLE = "Flask REST API Template"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Logging
    LOG_LEVEL = "DEBUG"
    DATE_FMT = "%Y-%m-%d %H:%M:%S"
    LOG_FILE_API = f"{base_dir}/logs/api.log"

    # Database configuration
    DB_ENGINE = env("DB_ENGINE")
    DB_USERNAME = env("DB_USERNAME", default=None)
    DB_PASSWORD = env("DB_PASSWORD", default=None)
    DB_HOST = env("DB_HOST", default=None)
    DB_PORT = env("DB_PORT", default=None)
    DB_NAME = env("DB_NAME")

    if DB_ENGINE == "sqlite":
        SQLALCHEMY_DATABASE_URI = f"{DB_ENGINE}:///{base_dir}/{DB_NAME}"
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"{DB_ENGINE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )


class DevelopmentConfig(Config):
    # False to disable CSRF protection during tests
    WTF_CSRF_ENABLED = False

    LOG_FILE_API = f"{Config.base_dir}/logs/api_dev.log"


class TestingConfig(Config):
    # Flask disables error catching during request handling for better error reporting in tests
    TESTING = True

    # False to disable CSRF protection during tests
    WTF_CSRF_ENABLED = False

    LOG_FILE_API = f"{Config.base_dir}/logs/api_test.log"


class ProductionConfig(Config):
    pass


config_dict = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
