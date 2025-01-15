from sqlalchemy import delete, func, select
from app.repositories.baserepository import CRUDRepository
# from app.database import get_session
from app.database import get_async_session
from app.models import Product

class ProductRepository(CRUDRepository):

    async def create(self, data: dict):
        async with get_async_session() as db:
            product = Product(**data)
            db.add(product)
            await db.commit()
            return product.id

    async def get_id(self, id: int):
        async with get_async_session() as db:
            query = select(Product).where(Product.id == int(id))
            product = await db.execute(query)
            return product.scalars().first()

    async def get_search(self, search: str):
        async with get_async_session() as db:
            query = select(Product).where(func.to_tsvector(Product.name).match(search))
            products = await db.execute(query)
            return products.scalars().all()

    async def getall(self):
        async with get_async_session() as db:
            return await db.query(Product).all()

    async def update(self, product: Product, data: dict):
        async with get_async_session() as db:
            for key, value in data.items():
                setattr(product, key, value)
            
            db.add(product)
            await db.commit()
            await db.refresh(product)

            return None

    async def delete(self, id: int):
        async with get_async_session() as db:
            query = delete(Product).where(Product.id == id)
            await db.execute(query)
            await db.commit()