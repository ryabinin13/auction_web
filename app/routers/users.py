from fastapi import APIRouter, BackgroundTasks, Depends, Response
from app.dependencies import get_current_user
from app.repositories.userrepository import UserRepository
from app.services.userservice import UserService
from app.auth import config
from app.schemas import BetBody, ProductBody
from app.models import User

user_router = APIRouter(tags=["User"])

@user_router.get("/logout")
def logout(response: Response, current_user_id: int = Depends(get_current_user)):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Вы вышли из системы"}

@user_router.get("/my_products")
async def get_all_products(current_user_id: int = Depends(get_current_user)):
    return await UserService().my_products(current_user_id)

@user_router.get("/check_product")
async def get_product(product_id : int, current_user_id: int = Depends(get_current_user)):
    return await UserService().check_product(product_id)

@user_router.delete("/delete_product")
async def delete_product(product_id : int, current_user_id: int = Depends(get_current_user)):
    return await UserService().delete_product(current_user_id, product_id)

@user_router.post("/start_auction")
async def start_auction(productbody: ProductBody, bg: BackgroundTasks, current_user_id: int = Depends(get_current_user)):
    return await UserService().start_auction(productbody, current_user_id, bg)


@user_router.post("/make_bet")
async def make_bet(product_id : int, betbody: BetBody, current_user_id: int = Depends(get_current_user)):
    return await UserService().create_bet(current_user_id, product_id, betbody)


@user_router.get("/search")
async def search(query: str, current_user_id: int = Depends(get_current_user)):
    return await UserService().search_product(query)