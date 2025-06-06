from fastapi import FastAPI
from app.routers.users import user_router
from app.routers.home import home_router
# from app.database import Base, engine
from app.db.database import Base, async_engine
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"]
)

app.include_router(user_router)
app.include_router(home_router)

# Base.metadata.create_all(async_engine)
async def create_database():
    async with async_engine.begin() as conn: # используется асинхронный контекстный менеджер
      await conn.run_sync(Base.metadata.create_all) # выполняем создание таблиц синхронно

@app.on_event("startup")
async def startup_event():
    await create_database()

