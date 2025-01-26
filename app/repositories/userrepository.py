from app.db.models import User
from app.db.database import get_async_session
# from app.database import get_session
from app.repositories.baserepository import CRUDRepository, GetUserEmail
from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session

class UserRepository(CRUDRepository, GetUserEmail):

    def __init__(self, async_session: Session):
        self.async_session = async_session

    async def create(self, data: dict):
        async with self.async_session as db:
            user = User(**data)
            db.add(user)
            await db.commit() 
            return user.id

    async def get_id(self, id: int) -> User:
        async with self.async_session as db:
            query = select(User).where(User.id == id)
            result = await db.execute(query)
            user = result.scalar_one_or_none()
            return user

    async def get_email(self, email: str) -> User:
        async with self.async_session as db:
            query = select(User).where(User.email == email)
            result = await db.execute(query)
            user = result.scalar_one_or_none()
            return user

    async def getall(self):
        async with self.async_session as db:
            return await db.query(User).all()

    async def update(self, user: User, data: dict) -> None:
        async with self.async_session as db:
            for key, value in data.items():
                setattr(user, key, value)
            
            db.add(user)
            await db.commit()
            await db.refresh(user)

            return None

    async def delete(self, id: int) -> None:
        async with self.async_session as db:
            user = db.query(User).filter(User.id == id).delete()
            await db.commit()
            return None

    async def get_products(self, id: int):
        async with self.async_session as db:
            query = select(User).where(User.id == int(id)).options(selectinload(User.products_create))
            user = await db.execute(query)
            user = user.scalar_one_or_none()

            if user is None:
                return []

            return user.products_create

