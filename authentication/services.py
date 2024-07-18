from typing import Dict, List
from injector import inject, singleton
from .repositories import UserRepository
from .models import User


@singleton
class UserService:
    @inject
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, username: str, email: str, password: str) -> User:
        if self.user_repository.find_by_username(
            username
        ) or self.user_repository.find_by_email(email):
            raise ValueError("User already exists")

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        self.user_repository.save(new_user)
        return new_user

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.user_repository.find_by_email(email)
        if user and user.check_password(password):
            return user
        raise ValueError("Invalid email or password")

    def list_users(self, filters: Dict[str, str]) -> List[User]:
        return self.user_repository.list(filters)

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    def update_user(self, user_id: int, username: str, password: str) -> User:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        user.username = username
        if password:
            user.set_password(password)
        self.user_repository.save(user)
        return user

    def delete_user(self, user_id: int):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        self.user_repository.delete(user)
