from app.repositories.baserepository import CRUDRepository
from app import SessionLocal
from app.models import Product, User, Bet

class BetRepository(CRUDRepository):

    def __init__(self):
        self.db = SessionLocal()

    def create(self, data: dict, user: User, product: Product):
        bet = Bet(
            user_id = user.id,
            product_id = product.id, 
            bet_price = data['bet_price']
        )
        self.db.add(bet)
        self.db.commit()
        return bet.id

    def get_id(self, id: int):
        return self.db.query(Bet).where(Bet.id == id).first()


    def getall(self):
        return self.db.query(Bet).all()


    def update(self, id: int, data: dict):
        bet = self.db.query(Bet).filter(Bet.id == id).update(data)
        self.db.commit()
        return bet.id

    def delete(self, id: int):
        pass