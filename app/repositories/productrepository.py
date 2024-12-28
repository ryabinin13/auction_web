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
            user_id = user.id,
            start_date = data['start_date'],
            end_date = data['end_date'],
            start_price = data['start_price'],
            current_price = data['current_price']
        )
        self.db.add(product)
        self.db.commit()
        return product.id

    def get_id(self, id: int):
        product = self.db.query(Product).where(Product.id == id).first()
        return product


    def getall(self):
        return self.db.query(Product).all()


    def update(self, product: Product, data: dict):
        product = Product(
            id = product.id,
            name =  data['name'],
            discription = data['discription'],
            user_id = data['user_id'],
            start_date = data['start_date'],
            end_date = data['end_date'],
            start_price = data['start_price'],
            current_price = data['current_price'],
            status = data['status']
        )
        self.db.merge(product)
        self.db.commit()
        return product

    def delete(self, id: int):
        product = self.db.query(Product).filter(Product.id == id).delete()
        self.db.commit()