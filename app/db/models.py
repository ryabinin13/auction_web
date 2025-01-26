from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base
from datetime import datetime, date
import enum


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[str]
    birthday: Mapped[date]
    phone_number: Mapped[str]

    products_create: Mapped[list["Product"]] = relationship(
        "Product", back_populates="user_create", foreign_keys="[Product.user_id]"
    )
    products_won: Mapped[list["Product"]] = relationship(
        "Product", back_populates="user_winner", foreign_keys="[Product.current_winner_id]"
    )
    user_bids: Mapped[list["Bet"]] = relationship(back_populates="user_bet")

class ProductStatus(enum.Enum):
        ACTIVE = "active"
        COMPLETED = "completed"

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    discription: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    start_price: Mapped[int]
    current_price: Mapped[int]
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]
    status: Mapped[ProductStatus] = mapped_column(Enum(ProductStatus), default=ProductStatus.ACTIVE)
    current_winner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))


    user_create: Mapped["User"] = relationship(
        "User", back_populates="products_create", foreign_keys="[Product.user_id]"
    )
    user_winner: Mapped["User"] = relationship(
        "User", back_populates="products_won", foreign_keys="[Product.current_winner_id]"
    )
    product_bids: Mapped[list["Bet"]] = relationship(back_populates="product_bet")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'discription': self.discription,
            'user_id': self.user_id,
            'start_price': self.start_price,
            'current_price': self.current_price,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'status': self.status,
            'current_winner_id': self.current_winner_id
         }


class Bet(Base):
    __tablename__ = "bids"

    id: Mapped[int] = mapped_column(primary_key=True)
    bet_price: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    product_bet: Mapped["Product"] = relationship(back_populates="product_bids")
    user_bet: Mapped["User"] = relationship(back_populates="user_bids")