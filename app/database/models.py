from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String())
    phone: Mapped[str] = mapped_column(String())


