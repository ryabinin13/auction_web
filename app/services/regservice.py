from app.repositories.userrepository import UserRepository
from app.schemas import RegistrationBody
from werkzeug.security import generate_password_hash
from fastapi import HTTPException, Request
from app.auth import config
from app.settings import Settings
from exceptions import UserAlreadyLoggedException, UserAlreadyHasEmailException, MinLenPasswordException, DifferentPasswordsException

class RegistrationService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def registration(self, data: RegistrationBody, request: Request) -> int:
        token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
        if token:
            raise UserAlreadyLoggedException
        
        if await self.user_repository.get_email(data.email):
            raise UserAlreadyHasEmailException
        
        if len(data.password1) < Settings.MIN_LEN_PASSWORD:
            raise MinLenPasswordException
        
        if not data.password1 == data.password2:
            raise DifferentPasswordsException

        password_hash = generate_password_hash(data.password1)
        data_dict = data.model_dump(exclude={"password1", "password2"})
        data_dict["password_hash"] = password_hash

        return await self.user_repository.create(data_dict)