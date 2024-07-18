from .models import User
from .repositories import UserRepository
from injector import singleton, inject


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
