import pytest

class FakeUserRepository:
    pass

@pytest.fixture
def get_user_repository():
    return FakeUserRepository()