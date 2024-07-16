import environ

env = environ.Env()


class Config(object):
    SQLALCHEMY_DATABASE_URI = env("DATABASE_URI")
    DEBUG = env.bool("DEBUG", default=False)
    apps = ["authentication"]


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass
