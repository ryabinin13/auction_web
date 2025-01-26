from sqlalchemy import delete, func, select
from app.repositories.baserepository import CRUDRepository
# from app.database import get_session
from app.db.database import get_async_session
from app.db.models import Product
from sqlalchemy.orm import selectinload, Session

class ProductRepository(CRUDRepository):
    def __init__(self, async_session: Session):
        self.async_session = async_session

    async def create(self, data: dict):
        async with self.async_session as db:
            product = Product(**data)
            db.add(product)
            await db.commit()
            return product.id

    async def get_id(self, id: int):
        async with self.async_session as db:
            query = select(Product).where(Product.id == int(id))
            product = await db.execute(query)
            return product.scalars().first()

    async def get_search(self, search: str):
        async with self.async_session as db:
            query = select(Product).where(func.to_tsvector(Product.name).match(search))
            products = await db.execute(query)
            return products.scalars().all()

    async def getall(self):
        async with self.async_session as db:
            return await db.query(Product).all()

    async def update(self, product: Product, data: dict):
        async with self.async_session as db:
            for key, value in data.items():
                setattr(product, key, value)
            
            db.add(product)
            await db.commit()
            await db.refresh(product)

            return None

    async def delete(self, id: int):
        async with self.async_session as db:
            query = delete(Product).where(Product.id == id)
            await db.execute(query)
            await db.commit()


    async def get_bids(self, id: int):
        async with self.async_session as db:
            query = select(Product).where(Product.id == int(id)).options(selectinload(Product.product_bids))
            product = await db.execute(query)
            product = product.scalar_one_or_none()

            if product is None:
                return []

            return product.product_bids