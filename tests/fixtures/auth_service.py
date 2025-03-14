from app.services.authservice import AuthService
from tests.fixtures.user_repository import get_user_repository
import pytest

@pytest.fixture
def auth_service(get_user_repository):
    return AuthService(
        user_repository=get_user_repository,
    )