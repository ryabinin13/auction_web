from fastapi import APIRouter, HTTPException, Response, Depends, Cookie 
from app.services.regservice import RegistrationService
from app.services.authservice import AuthService
from app.schemas import RegistrationBody, LoginBody
from app import config, security


home_router = APIRouter()

@home_router.post("/registration")
def registration(data: RegistrationBody):
    return RegistrationService().registration(data)


@home_router.post("/login")
def login(loginbody: LoginBody, response: Response):
    user = AuthService().authenticate_user(loginbody)
    token = AuthService().generate_token(user)
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    return {"access_token": token}

   
