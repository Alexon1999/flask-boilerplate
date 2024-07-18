from datetime import datetime
from typing import List
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone
from .models import User
from injector import singleton, inject

# Repository Pattern : The Repository pattern is used to abstract the data access layer, providing a consistent API for accessing and manipulating data. This separates the business logic from direct database operations, making the codebase easier to manage and test also making it easier to change the underlying data source without affecting the business logic.

# The UserRepository class encapsulates all interactions with the User table in the database, using SQLAlchemy for ORM operations.

# Singleton Pattern : The Singleton pattern is used to ensure that only one instance of a class is created and that instance is reused whenever the class is injected into other parts of your application. This can help reduce memory usage and improve performance.


# use the @singleton decorator from the injector package, it designates a class as a singleton within the scope of the dependency injection container. This means that only one instance of the class will be created and that instance will be reused whenever the class is injected into other parts of your application.

# Summary
# Repository Pattern: Encapsulates data access logic in a separate layer.
# Singleton Pattern: Ensures only one instance of UserRepository and UserService is created and reused.
# Dependency Injection: Uses Flask-Injector to automatically inject dependencies into classes, improving modularity and testability.


@singleton
class UserRepository:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def list(self, filters: dict) -> List[User]:
        query = self.db.select(User)
        if "username" in filters:
            query = query.filter(
                User.username.like(f"%{filters['username']}%")
            )
        if "email" in filters:
            query = query.filter(User.email.like(f"%{filters['email']}%"))
        return self.db.session.execute(query).scalars().all()

    def save(self, user: User):
        self.db.session.add(user)
        self.db.session.commit()

    def delete(self, user: User):
        self.db.session.delete(user)
        self.db.session.commit()

    def update(self, username: str, user: User):
        user.username = username
        user.updated_at = datetime.datetime.now(timezone.utc)
        self.db.session.commit()

    def find_by_email(self, email: str) -> User:
        return self.db.session.execute(
            self.db.select(User).filter_by(email=email)
        ).scalar()

    def find_by_username(self, username: str) -> User:
        return self.db.session.execute(
            self.db.select(User).filter_by(username=username)
        ).scalar()

    def find_by_id(self, user_id: int) -> User:
        return self.db.session.execute(
            self.db.select(User).filter_by(id=user_id)
        ).scalar()
