from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from app.repositories.userrepository import UserRepository
from app.services.regservice import RegistrationService
from app.services.authservice import AuthService
from app.schemas import RegistrationBody, LoginBody
from app.auth import config
from app.dependencies import get_auth_service, get_current_user, get_reg_service, get_user_repository, get_user_service
from app.services.userservice import UserService


home_router = APIRouter(tags=["Auth"], prefix='/auth')

@home_router.post("/register")
async def registration(
    data: RegistrationBody,
    request: Request,
    reg_service: Annotated[RegistrationService, Depends(get_reg_service)]
    ):
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    if not token:
        return await reg_service.registration(data)
    raise HTTPException(status_code=403, detail="Сначала выйдете из системы")
    

@home_router.post("/login")
async def login(
    loginbody: LoginBody,
    response: Response,
    request: Request,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
    ):
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    if not token:
        user = await auth_service.authenticate_user(loginbody)
        token = auth_service.generate_token(user)
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=403, detail="Сначала выйдете из системы")

@home_router.delete("/logout")
def logout(
    response: Response,
    current_user_id: int = Depends(get_current_user)
    ):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Вы вышли из системы"}
