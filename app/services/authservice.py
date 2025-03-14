from datetime import datetime, timedelta
from app.repositories.userrepository import UserRepository
from app.schemas import LoginBody
from werkzeug.security import check_password_hash
from fastapi import HTTPException, Request, Response
from app.auth import security, config
from app.db.models import User
from app.settings import Settings
from exceptions import UserEmailNotFoundException, UserNotCorrectPasswordException, UserAlreadyLoggedException
import jwt

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate_user(self, loginbody: LoginBody) -> User:
        user = await self.user_repository.get_email(loginbody.email)
        if not user:
            raise UserEmailNotFoundException
        if not check_password_hash(user.password_hash, loginbody.password):
            raise UserNotCorrectPasswordException
        return user

    async def generate_token(self, user_id: int):
        payload = {
            "uid": str(user_id),
            "exp": datetime.utcnow() + timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRES) 
        }
        try:
            encoded_jwt = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
            return encoded_jwt
        except Exception as e:
            raise 
        
    async def login_user(self, loginbody: LoginBody, response: Response, request: Request) -> dict:
        token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
        if not token:
            user = await self.authenticate_user(loginbody)
            token = await self.generate_token(user.id)
            response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
            return {"access_token": token}
        raise UserAlreadyLoggedException
    
