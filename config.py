import os
import environ

env = environ.Env()


class Config(object):
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # Database configuration
    DB_ENGINE = env("DB_ENGINE")
    DB_USERNAME = env("DB_USERNAME")
    DB_PASSWORD = env("DB_PASSWORD")
    DB_HOST = env("DB_HOST")
    DB_PORT = env("DB_PORT")
    DB_NAME = env("DB_NAME")

    if DB_ENGINE == "sqlite":
        SQLALCHEMY_DATABASE_URI = f"{DB_ENGINE}:///{base_dir}/{DB_NAME}"
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"{DB_ENGINE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    DEBUG = env.bool("DEBUG", default=False)
    installed_apps = ["authentication"]


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass
