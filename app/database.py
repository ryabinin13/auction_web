from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
import os
from dotenv import load_dotenv

load_dotenv()

url_database = os.getenv("DATABASE_URL")

# engine = create_engine(
#     url=url_database,
#     echo=False
# )

#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_session():
#    return SessionLocal()

async_engine = create_async_engine(
    url=url_database,
    echo=False
)
get_async_session = async_sessionmaker(async_engine, autocommit=False, autoflush=False, expire_on_commit=False)

# async def get_async_session():
#     async with async_session_local() as session:
#         yield session

Base = declarative_base()





