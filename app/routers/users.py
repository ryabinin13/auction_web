from fastapi import APIRouter, Depends, HTTPException, Request, Response
from app.dependencies import get_current_user
from app.services.userservice import UserService
from app.services.authservice import AuthService
from app import security, config
from app.schemas import ProductBody
from app.models import User

user_router = APIRouter()


@user_router.get("/logout")
def logout(response: Response, current_user: User = Depends(get_current_user)):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Successfully logged out"}


@user_router.get("/getid")
def get_id(id, current_user: User = Depends(get_current_user)):
    return UserService().get_user_id(id)


@user_router.get("/getemail")
def get_email(email, current_user: User = Depends(get_current_user)):
    return UserService().get_user_email(email)

@user_router.post("/createproduct")
def create_product(productbody: ProductBody, current_user: User = Depends(get_current_user)):
    return UserService().create_product(productbody, current_user)


@user_router.get("/getallproducts")
def getallproducts(current_user: User = Depends(get_current_user)):
    return current_user.products