import pytest
from unittest.mock import MagicMock
from authentication.models import User
from authentication.services import UserService
from tests.authentication.data.mock_user_repositories import MockUserRepository


@pytest.fixture
def mock_user_repository():
    return MockUserRepository()


@pytest.fixture
def user_service(mock_user_repository):
    return UserService(user_repository=mock_user_repository)


class TestUserServiceWithMock:
    def test_create_user(self, user_service, mock_user_repository):
        mock_user_repository.find_by_email = MagicMock(return_value=None)
        mock_user_repository.find_by_username = MagicMock(return_value=None)

        user = user_service.create_user(
            "testuser", "test@example.com", "password"
        )

        assert user is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"

    def test_create_user_existing_email(
        self, user_service, mock_user_repository
    ):
        existing_user = User(username="existinguser", email="test@example.com")
        mock_user_repository.find_by_email = MagicMock(
            return_value=existing_user
        )

        with pytest.raises(ValueError):
            user_service.create_user("newuser", "test@example.com", "password")

    def test_create_user_existing_username(
        self, user_service, mock_user_repository
    ):
        existing_user = User(username="existinguser", email="test@example.com")
        mock_user_repository.find_by_email = MagicMock(
            return_value=existing_user
        )

        with pytest.raises(ValueError):
            user_service.create_user("newuser", "test@example.com", "password")
