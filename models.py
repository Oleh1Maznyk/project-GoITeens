from typing import Optional, List

from sqlalchemy import String, DateTime, JSON, create_engine, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import bcrypt
from datetime import datetime


Base = declarative_base()
db = SQLAlchemy(model_class=Base, engine_options=dict(echo=True))


class User(Base, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    phone_number: Mapped[str] = mapped_column(String(20))
    first_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(120), nullable=True, default=None)
    password_: Mapped[str] = mapped_column(String(128))
    active: Mapped[bool] = mapped_column(Boolean(), default=True)

    @property
    def password(self):
        return self.password_

    @password.setter
    def password(self, pwd):
        self.password_ = generate_password_hash(pwd)

    def is_verify_password(self, pwd):
        return check_password_hash(self.password_, pwd)


class Menu(Base):
    __tablename__ = "menu"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(20), unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text(), nullable=True, default=None)
    price: Mapped[int] = mapped_column()
    active: Mapped[bool] = mapped_column(Boolean(), default=True)


class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_list: Mapped[dict] = mapped_column(JSONB)
    order_time: Mapped[datetime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user = relationship("User", foreign_keys="Orders.user_id")