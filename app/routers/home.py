from fastapi import APIRouter, HTTPException, Response, Request
from app.services.regservice import RegistrationService
from app.services.authservice import AuthService
from app.schemas import RegistrationBody, LoginBody
from app.auth import config


home_router = APIRouter(tags=["Auth"])

@home_router.post("/registration")
async def registration(data: RegistrationBody, request: Request):
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    if not token:
        return await RegistrationService().registration(data)
    raise HTTPException(status_code=403, detail="Сначала выйдете из системы")
    


@home_router.post("/login")
async def login(loginbody: LoginBody, response: Response, request: Request):
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    if not token:
        user = await AuthService().authenticate_user(loginbody)
        token = AuthService().generate_token(user)
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=403, detail="Сначала выйдете из системы")

   
