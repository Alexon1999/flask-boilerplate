from flask_injector import FlaskInjector
from flask_sqlalchemy import SQLAlchemy
from .db import db
from injector import Binder, singleton


def init_injections(app):
    FlaskInjector(app=app, modules=[configure])


def configure(binder: Binder):
    # create a singleton binding for the SQLAlchemy instance
    # we can inject this instance into other parts of our application
    binder.bind(SQLAlchemy, to=db, scope=singleton)
