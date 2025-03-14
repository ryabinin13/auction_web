import jwt
from app.auth import config
from fastapi import HTTPException, Request
from app.repositories.betrepository import BetRepository
from app.repositories.productrepository import ProductRepository
from app.repositories.userrepository import UserRepository
from app.db.database import get_async_session
from app.services.authservice import AuthService
from app.services.regservice import RegistrationService
from app.services.userservice import UserService


def get_current_user(request: Request):
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")

    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM]) 
        user_id = payload.get("uid")
        if user_id is None:
            raise ValueError("Invalid token payload: 'uid' claim not found")
        # user = UserRepository().get_id(user_id)
        # if not user:
        #     raise HTTPException(status_code=401, detail="User not found")
        return int(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")
    

def get_user_repository() -> UserRepository:
    async_session = get_async_session()
    return UserRepository(async_session)

def get_product_repository() -> ProductRepository:
    async_session = get_async_session()
    return ProductRepository(async_session)

def get_bet_repository() -> BetRepository:
    async_session = get_async_session()
    return BetRepository(async_session)
                         
def get_user_service() -> UserService:
    return UserService(
        user_repository=get_user_repository(),
        product_repository=get_product_repository(),
        bet_repository=get_bet_repository()
    )

def get_auth_service() -> AuthService:
    return AuthService(
        user_repository=get_user_repository(),
    )

def get_reg_service() -> RegistrationService:
    return RegistrationService(
        user_repository=get_user_repository(),
    )