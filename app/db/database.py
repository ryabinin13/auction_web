from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
import os
from dotenv import load_dotenv

load_dotenv()

url_database = os.getenv("DATABASE_URL")

async_engine = create_async_engine(
    url=url_database,
    echo=False
)
get_async_session = async_sessionmaker(async_engine, autocommit=False, autoflush=False, expire_on_commit=False)

Base = declarative_base()





