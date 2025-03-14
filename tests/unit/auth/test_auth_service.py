import jwt
from app.db.models import User
from app.services.authservice import AuthService
from tests.fixtures.auth_service import auth_service
from app.auth import config
import pytest

async def test_generate_token_success(auth_service):
    user_id = 1
    token = await auth_service.generate_token(user_id)
    payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
    assert user_id == int(payload.get("uid"))
