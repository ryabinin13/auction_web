from app.repositories.baserepository import CRUDRepository
from app.database import get_session
from app.models import Product, User, Bet

class BetRepository(CRUDRepository):

    def create(self, data: dict, user: User, product: Product):
        with get_session() as db:
            bet = Bet(
                user_id = user.id,
                product_id = product.id, 
                bet_price = data['bet_price']
            )
            db.add(bet)
            db.commit()
            return bet.id

    def get_id(self, id: int):
        with get_session() as db:
            return db.query(Bet).where(Bet.id == id).first()


    def getall(self):
        with get_session() as db:
            return db.query(Bet).all()


    def update(self, id: int, data: dict):
        with get_session() as db:
            bet = self.db.query(Bet).filter(Bet.id == id).update(data)
            db.commit()
            return bet.id

    def delete(self, id: int):
        pass