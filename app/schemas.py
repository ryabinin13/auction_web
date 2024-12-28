from pydantic import BaseModel, EmailStr
from datetime import date
from datetime import datetime

class RegistrationBody(BaseModel):
    username: str
    email: EmailStr
    birthday: date
    phone_number: str
    password1: str
    password2: str

class LoginBody(BaseModel):
    email: EmailStr
    password: str

class ProductBody(BaseModel):
    name: str
    discription: str
    start_price: int
    end_date: datetime


class BetBody(BaseModel):
    bet_price: int
    