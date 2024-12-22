from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.security import OAuth2PasswordBearer
from authx import AuthX, AuthXConfig

app = FastAPI()
config = AuthXConfig()

config.JWT_SECRET_KEY = "JWT_TOKEN_AUCTION_WEB"
config.JWT_ACCESS_COOKIE_NAME = "auction_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ALGORITHM = "HS256"
config.JWT_ACCESS_TOKEN_EXPIRES = 30

security = AuthX(config=config)

DATABASE_URL = "postgresql://postgres:stud@localhost:5432/auction"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


from app import models
from app.routers import home, users