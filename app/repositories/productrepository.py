from app.repositories.baserepository import CRUDRepository
from app.database import get_session
from app.models import Product, User

class ProductRepository(CRUDRepository):

    def create(self, data: dict, user: User):
        with get_session() as db:
            product = Product(
                name =  data['name'],
                discription = data['discription'],
                user_id = user.id,
                start_date = data['start_date'],
                end_date = data['end_date'],
                start_price = data['start_price'],
                current_price = data['current_price'],
                current_winner_id = None
            )
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
            product = Product(
                id = product.id,
                name =  data['name'],
                discription = data['discription'],
                user_id = data['user_id'],
                start_date = data['start_date'],
                end_date = data['end_date'],
                start_price = data['start_price'],
                current_price = data['current_price'],
                status = data['status'],
                current_winner_id = data['current_winner_id']
            )
            db.merge(product)
            db.commit()
            return product

    def delete(self, id: int):
        with get_session() as db:
            product = self.db.query(Product).filter(Product.id == id).delete()
            db.commit()