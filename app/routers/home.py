from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from app.services.regservice import RegistrationService
from app.services.authservice import AuthService
from app.schemas import RegistrationBody, LoginBody
from app.auth import config
from app.settings import Settings
from app.dependencies import get_auth_service, get_current_user, get_reg_service
from exceptions import UserEmailNotFoundException, UserNotCorrectPasswordException, UserAlreadyLoggedException, UserAlreadyHasEmailException, MinLenPasswordException, DifferentPasswordsException
from fastapi.responses import RedirectResponse

home_router = APIRouter(tags=["Auth"])

@home_router.post("/register")
async def registration(
    data: RegistrationBody,
    request: Request,
    reg_service: Annotated[RegistrationService, Depends(get_reg_service)]
    ) -> int:
    try:
        return await reg_service.registration(data, request)
    except UserAlreadyLoggedException as e:
        raise HTTPException(status_code=403, detail="Сначала выйдете из системы")
    
    except UserAlreadyHasEmailException as e:
        raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует")
    
    except MinLenPasswordException as e:
        raise HTTPException(status_code=400, detail=f"Минимальная длина пароля должна быть равна {Settings.MIN_LEN_PASSWORD}")

    except DifferentPasswordsException as e:
        raise HTTPException(status_code=400, detail="Пароли не совпадают")
    
    

@home_router.post("/login")
async def login(
    loginbody: LoginBody,
    response: Response,
    request: Request,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
    ):
    try:       
        token = await auth_service.login_user(loginbody, response, request)
    except UserEmailNotFoundException as e:
        raise HTTPException(status_code=404, detail="Пользователя с таким email не существует")
    
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail="Неверный пароль")
    
    except UserAlreadyLoggedException as e:
        raise HTTPException(status_code=403, detail="Сначала выйдете из системы")
    
    return {"token": token}

@home_router.delete("/logout")
def logout(
    response: Response
    ):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Вы вышли из системы"}


