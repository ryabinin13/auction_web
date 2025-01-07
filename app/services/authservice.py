from datetime import datetime, timedelta
from app.repositories.userrepository import UserRepository
from app.schemas import LoginBody
from werkzeug.security import check_password_hash
from fastapi import HTTPException, Request
from app.auth import security, config
from app.models import User
import jwt

class AuthService:

    def authenticate_user(self, loginbody: LoginBody):
        user = UserRepository().get_email(loginbody.email)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователя с таким email не существует")
        if not check_password_hash(user.password_hash, loginbody.password):
            raise HTTPException(status_code=401, detail="Неверный пароль")
        return user

    def generate_token(self, user: User):
        payload = {
            "uid": str(user.id),
            "exp": datetime.utcnow() + timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRES) # исправлено
        }
        try:
            encoded_jwt = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
            return encoded_jwt
        except Exception as e:
            raise 
        
    

