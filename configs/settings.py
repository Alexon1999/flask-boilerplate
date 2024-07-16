import os
import environ

env = environ.Env()

INSTALLED_APPS = [
    "authentication",
]


class Config(object):
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # Database configuration
    DB_ENGINE = env("DB_ENGINE")
    DB_USERNAME = env("DB_USERNAME", default=None)
    DB_PASSWORD = env("DB_PASSWORD", default=None)
    DB_HOST = env("DB_HOST", default=None)
    DB_PORT = env("DB_PORT", default=None)
    DB_NAME = env("DB_NAME")

    try:
        if DB_ENGINE == "sqlite":
            SQLALCHEMY_DATABASE_URI = f"{DB_ENGINE}:///{base_dir}/{DB_NAME}"
        else:
            SQLALCHEMY_DATABASE_URI = f"{DB_ENGINE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    except Exception as e:
        print("Database Connection error: ", e)

    DEBUG = env.bool("DEBUG", default=False)
    INSTALLED_APPS = INSTALLED_APPS


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config_dict = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
