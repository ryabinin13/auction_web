from app.repositories.userrepository import UserRepository
from app.schemas import RegistrationBody
from werkzeug.security import generate_password_hash
from fastapi import HTTPException

class RegistrationService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def registration(self, data: RegistrationBody):
        if await self.user_repository.get_email(data.email):
            raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует")
        if len(data.password1) < 6:
            raise HTTPException(status_code=400, detail="Минимальная длина пароля должна быть равна 6")
        if not data.password1 == data.password2:
            raise HTTPException(status_code=400, detail="Пароли не совпадают")

        password_hash = generate_password_hash(data.password1)
        data_dict = data.model_dump(exclude={"password1", "password2"})
        data_dict["password_hash"] = password_hash

        return await self.user_repository.create(data_dict)