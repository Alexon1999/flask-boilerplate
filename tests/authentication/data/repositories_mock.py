from datetime import datetime
from pytz import timezone
from authentication.models import User


class MockUserRepository:
    def __init__(self):
        self.users = []
        self.current_id = 1

    def save(self, user: User):
        if not user.id:
            user.id = self.current_id
            self.current_id += 1
            self.users.append(user)
        else:
            for idx, existing_user in enumerate(self.users):
                if existing_user.id == user.id:
                    self.users[idx] = user
                    break

    def delete(self, user: User):
        self.users = [
            existing_user
            for existing_user in self.users
            if existing_user.id != user.id
        ]

    def update(self, username: str, user: User):
        for existing_user in self.users:
            if existing_user.id == user.id:
                existing_user.username = username
                existing_user.updated_at = datetime.now(timezone.utc)
                break

    def find_by_email(self, email: str) -> User:
        for user in self.users:
            if user.email == email:
                return user
        return None

    def find_by_username(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        return None

    def find_by_id(self, user_id: int) -> User:
        for user in self.users:
            if user.id == user_id:
                return user
        return None
