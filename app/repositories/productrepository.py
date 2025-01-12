from app.repositories.baserepository import CRUDRepository
from app.database import get_session
from app.models import Product, User

class ProductRepository(CRUDRepository):

    def create(self, data: dict, user: User):
        with get_session() as db:
            product = Product(**data)
            db.add(product)
            db.commit()
            return product.id

    def get_id(self, id: int):
        with get_session() as db:
            product = db.query(Product).where(Product.id == id).first()
            return product


    def getall(self):
        with get_session() as db:
            return db.query(Product).all()


    def update(self, product: Product, data: dict):
        with get_session() as db:
            product = Product(**data)
            db.merge(product)
            db.commit()
            return product

    def delete(self, id: int):
        with get_session() as db:
            product = self.db.query(Product).filter(Product.id == id).delete()
            db.commit()