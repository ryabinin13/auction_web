from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response
from app.dependencies import get_current_user, get_user_service
from app.repositories.userrepository import UserRepository
from app.services.userservice import UserService
from app.auth import config
from app.schemas import BetBody, ProductBody
from app.db.models import Product, User
from exceptions import ProductNotFoundException, AuctionCompletedException, UserNotCorrectBetException

user_router = APIRouter(tags=["User"])

@user_router.get("/me/products")
async def get_all_products(
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user_id: int = Depends(get_current_user),
    ):
    return await user_service.my_products(current_user_id)

@user_router.get("/products/{product_id}")
async def get_product(
    product_id : int,
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user_id: int = Depends(get_current_user)
    ):
    return await user_service.check_product(product_id)

@user_router.delete("/products/{product_id}")
async def delete_product(
    product_id : int,
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user_id: int = Depends(get_current_user)
    ) -> None:
    try:
        return await user_service.delete_product(current_user_id, product_id)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=404, detail="Товар не найден")

@user_router.post("/products")
async def start_auction(
    productbody: ProductBody,
    bg: BackgroundTasks,
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user_id: int = Depends(get_current_user)
    ) -> int:
    return await user_service.start_auction(productbody, current_user_id, bg)


@user_router.post("/bids")
async def make_bet(
    product_id : int,
    betbody: BetBody,
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user_id: int = Depends(get_current_user)
    ) -> int:
    try:
        return await user_service.create_bet(current_user_id, product_id, betbody)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=404, detail="Товар не найден")
    except AuctionCompletedException as e:
        raise HTTPException(status_code=400, detail="Аукцион завершен")
    except UserNotCorrectBetException as e:
        raise HTTPException(status_code=400, detail="Ставка дожна быть выше, чем текущая")

@user_router.get("/products")
async def search(
    query: str,
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user_id: int = Depends(get_current_user)
    ):
    return await user_service.search_product(query)