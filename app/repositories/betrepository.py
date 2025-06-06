from sqlalchemy import delete, select
from app.repositories.baserepository import CRUDRepository
# from app.database import get_session
from app.db.database import get_async_session
from app.db.models import Bet
from sqlalchemy.orm import selectinload, Session

class BetRepository(CRUDRepository):
    def __init__(self, async_session: Session):
        self.async_session = async_session

    async def create(self, data: dict) -> int:
        async with self.async_session as db:
            bet = Bet(**data)
            db.add(bet)
            await db.commit()
            return bet.id

    async def get_id(self, id: int) -> Bet:
        async with self.async_session as db:
            query = select(Bet).where(Bet.id == int(id))
            bet = await db.execute(query)
            return bet.scalars().first()


    async def getall(self) -> list[Bet]:
        async with self.async_session as db:
            return db.query(Bet).all()


    async def update(self, bet: Bet, data: dict) -> int:
         async with self.async_session as db:
            for key, value in data.items():
                setattr(bet, key, value)
            
            db.add(bet)
            await db.commit()
            await db.refresh(bet)

            return None

    async def delete(self, id: int) -> None:
        async with self.async_session as db:
            query = delete(Bet).where(Bet.id == id)
            await db.execute(query)
            await db.commit()
            return None