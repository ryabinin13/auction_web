from fastapi import APIRouter, BackgroundTasks, Depends, Response
from app.dependencies import get_current_user
from app.repositories.userrepository import UserRepository
from app.services.userservice import UserService
from app.auth import config
from app.schemas import BetBody, ProductBody
from app.models import User

user_router = APIRouter(tags=["User"])

@user_router.get("/logout")
def logout(response: Response, current_user: User = Depends(get_current_user)):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Вы вышли из системы"}

@user_router.get("/my_products")
def get_all_products(current_user: User = Depends(get_current_user)):
    return current_user.products

@user_router.delete("/delete_product")
def delete_product(product_id : int, current_user: User = Depends(get_current_user)):
    return UserService().delete_product(current_user, product_id)

@user_router.post("/start_auction")
def start_auction(productbody: ProductBody, bg: BackgroundTasks, current_user: User = Depends(get_current_user)):
    return UserService().start_auction(productbody, current_user, bg)


@user_router.post("/make_bet")
def make_bet(product_id : int, betbody: BetBody, current_user: User = Depends(get_current_user)):
    return UserService().create_bet(current_user, product_id, betbody)


@user_router.get("/test")
def make_bet():
    return "hello"