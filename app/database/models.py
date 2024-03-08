from typing import List

from sqlalchemy import ForeignKey, String, BigInteger, Float, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String())
    phone: Mapped[str] = mapped_column(String())

    # cart_user: Mapped[List['Cart']] = relationship(back_populates='user_rel', cascade='all, delete')
    # order_rel: Mapped[List['Orders']] = relationship(back_populates='user_rel', cascade='all, delete')
    # collecting_rel: Mapped[List['Collecting_the_cake']] = relationship(back_populates='user_rel', cascade='all, delete')


