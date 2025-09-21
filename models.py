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
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(120), nullable=True, default=None)
    password_: Mapped[str] = mapped_column(String(128))
    active: Mapped[bool] = mapped_column(Boolean(), default=True)

    orders: Mapped[List["Orders"]] = relationship("Orders", back_populates="user")

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
    order_list: Mapped[dict] = mapped_column(JSON)
    order_time: Mapped[datetime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped["User"] = relationship("User", back_populates="orders")


def init_sample_data():
    if Menu.query.count() == 0:
        sample_menu = [

            # Кавові напої
            Menu(type='Еспресо', description='Класичний італійський еспресо з насиченим смаком', price=45, active=True),
            Menu(type='Капучино', description='Еспресо з ніжною молочною піною та корицею', price=65, active=True),
            Menu(type='Латте', description='Еспресо з великою кількістю молока та карамельним сиропом', price=70, active=True),
            Menu(type='Американо', description='Еспресо з гарячою водою, класичний американський стиль', price=50, active=True),
            Menu(type='Мокко', description='Шоколадний кавовий напій з вершками', price=75, active=True),
            Menu(type='Флет Вайт', description='Подвійний еспресо з мікропіною', price=68, active=True),

            # Десерти
            Menu(type='Чізкейк', description='Ніжний чізкейк з лісовими ягодами та м\'ятою', price=120, active=True),
            Menu(type='Тірамісу', description='Італійський десерт з маскарпоне та кавою', price=135, active=True),
            Menu(type='Шоколадний торт', description='Багатошаровий торт з темним шоколадом', price=110, active=True),
            Menu(type='Панна котта', description='Італійський десерт з ванільним кремом', price=95, active=True),

            # Випічка
            Menu(type='Круасан', description='Свіжий французький круасан з шоколадною начинкою', price=85, active=True),
            Menu(type='Маффін', description='Домашній маффін з чорницею та лимонною цедрою', price=65, active=True),
            Menu(type='Багет', description='Хрусткий французький багет з травами', price=45, active=True),
            Menu(type='Данішка', description='Данське тістечко з яблучною начинкою', price=75, active=True),

            # Холодні напої
            Menu(type='Фрапе', description='Холодний кавовий напій з льодом та вершками', price=80, active=True),
            Menu(type='Айс латте', description='Холодний латте з ванільним сиропом', price=75, active=True),
            Menu(type='Лимонад', description='Свіжий домашній лимонад з м\'ятою', price=55, active=True),
            Menu(type='Смузі', description='Фруктовий смузі з манго та бананом', price=85, active=True),
        ]

        try:
            for item in sample_menu:
                db.session.add(item)
            db.session.commit()
            print(f"Додано {len(sample_menu)} позицій до меню")
        except Exception as e:
            print(f"Помилка при додаванні даних: {e}")
            db.session.rollback()
