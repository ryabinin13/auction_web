from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app import Base
import enum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    password_hash = Column(String, index=True)
    birthday = Column(Date)
    phone_number = Column(String)

    products = relationship("Product", back_populates="user")
    bids = relationship("Bet", back_populates="user")


class ProductStatus(enum.Enum):
        ACTIVE = "active"
        COMPLETED = "completed"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    discription = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    start_price = Column(Integer)
    current_price = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(Enum(ProductStatus), default=ProductStatus.ACTIVE)

    user = relationship("User", back_populates="products")
    bids = relationship("Bet", back_populates="product")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'discription': self.discription,
            'user_id': self.user_id,
            'start_price': self.start_price,
            'current_price': self.current_price,
            'start_date': self.start_date,
            'end_date': self.end_date
         }

class Bet(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    bet_price = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id= Column(Integer, ForeignKey('products.id'))

    product = relationship("Product", back_populates="bids")
    user = relationship("User", back_populates="bids")