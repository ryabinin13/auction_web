import pytest
from unittest.mock import MagicMock
from app.db.models import User
from app.repositories.userrepository import UserRepository
from sqlalchemy.exc import SQLAlchemyError

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def user_repository(mock_session):
    repo = UserRepository()
    repo.db = mock_session
    return repo

def test_create_user_success(user_repository: UserRepository, mock_session: MagicMock):
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password_hash': 'hashed_password',
        'birthday': '2000-01-01',
         'phone_number': '1234567890',
    }
    new_user_email = user_repository.create(user_data)
    mock_session.add.assert_called()
    mock_session.commit.assert_called()
    assert new_user_email == 'test@example.com'  
