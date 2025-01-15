from sqlalchemy import select
from app.repositories.baserepository import CRUDRepository
# from app.database import get_session
from app.database import get_async_session
from app.models import Bet

class BetRepository(CRUDRepository):

    async def create(self, data: dict):
        async with get_async_session() as db:
            bet = Bet(**data)
            db.add(bet)
            await db.commit()
            return bet.id

    async def get_id(self, id: int):
        async with get_async_session() as db:
            query = select(Bet).where(Bet.id == int(id))
            bet = await db.execute(query)
            return bet.scalars().first()


    async def getall(self):
        async with get_async_session() as db:
            return db.query(Bet).all()


    async def update(self, id: int, data: dict):
        async with get_async_session() as db:
            bet = self.db.query(Bet).filter(Bet.id == id).update(data)
            db.commit()
            return bet.id

    def delete(self, id: int):
        pass