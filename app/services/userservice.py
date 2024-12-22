from fastapi import HTTPException
from app.models import User
from app.repositories.userrepository import UserRepository
from app.repositories.productrepository import ProductRepository
from app.schemas import ProductBody

class UserService:
    
    def get_user_id(self, id):
        user = UserRepository().get_id(id)
        return {"username": user.username, "birthaday": user.birthday, "email": user.email}
    

    def get_user_email(self, email):
        user = UserRepository().get_email(email)
        return {"username": user.username, "birthaday": user.birthday, "email": user.email}
    
    def create_product(self, data: ProductBody, user: User):
        data_dict = data.model_dump()
        return ProductRepository().create(data_dict, user)
