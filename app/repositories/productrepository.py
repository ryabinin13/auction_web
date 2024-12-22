from fastapi import HTTPException
from app.repositories.baserepository import CRUDRepository
from app import SessionLocal
from app.models import Product, User

class ProductRepository(CRUDRepository):

    def __init__(self):
        self.db = SessionLocal()

    def create(self, data: dict, user: User):
        product = Product(
            name =  data['name'],
            discription = data['discription'],
            user_id = user.id
        )
        self.db.add(product)
        self.db.commit()
        return product.id

    def get_id(self, id: int):
        return self.db.query(Product).where(Product.id == id).first()


    def getall(self):
        return self.db.query(Product).all()


    def update(self, id: int, data: dict):
        product = self.db.query(Product).filter(Product.id == id).update(data)
        self.db.commit()
        return product.id

    def delete(self, id: int):
        pass