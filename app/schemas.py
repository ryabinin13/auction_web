from pydantic import BaseModel, EmailStr
from datetime import date

class RegistrationBody(BaseModel):
    username: str
    email: EmailStr
    birthday: date
    password1: str
    password2: str

class LoginBody(BaseModel):
    email: EmailStr
    password: str

class ProductBody(BaseModel):
    name: str
    discription: str
    