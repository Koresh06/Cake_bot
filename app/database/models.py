from typing import List

from sqlalchemy import ForeignKey, String, BigInteger, Float, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker

from app.database.database import create_engine
from app.config_loader import create_config_from_toml


config = create_config_from_toml('/config/config.template.toml')

async_session = async_sessionmaker(create_engine(config))


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String())
    phone: Mapped[str] = mapped_column(String())

    cart_user: Mapped[List['Cart']] = relationship(back_populates='user_rel', cascade='all, delete')
    order_rel: Mapped[List['Orders']] = relationship(back_populates='user_rel', cascade='all, delete')
    collecting_rel: Mapped[List['Collecting_the_cake']] = relationship(back_populates='user_rel', cascade='all, delete')

class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String())
    count: Mapped[int] = mapped_column(Integer(), default=0)

    product_rel: Mapped[List['Product']] = relationship(back_populates='categories_rel', cascade='all, delete')   

class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    categories_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))
    name: Mapped[str] = mapped_column(String())
    image: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    price: Mapped[float] = mapped_column(Float())

    cartitem_rel: Mapped[List['CartItem']] = relationship(back_populates='product_rel', cascade='all, delete')
    categories_rel: Mapped['Categories'] = relationship(back_populates='product_rel')

class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))

    user_rel: Mapped['User'] = relationship(back_populates='cart_user')
    items: Mapped[List['CartItem']] = relationship(back_populates='cart_rel', cascade='all, delete')
    order_rel: Mapped[List['Orders']] = relationship(back_populates='cart_rel', cascade='all, delete')
    collecting_rel: Mapped[List['Collecting_the_cake']] = relationship(back_populates='cart_rel', cascade='all, delete')

class CartItem(Base):
    __tablename__ = 'cartitem'

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'))
    quantuty: Mapped[int] = mapped_column(default=1)


    cart_rel: Mapped['Cart'] = relationship(back_populates='items')
    product_rel: Mapped['Product'] = relationship(back_populates='cartitem_rel')
    

class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id', ondelete='CASCADE'))
    data_time: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column(String())
    order: Mapped[dict] = mapped_column(JSON())
    total_cost: Mapped[float] = mapped_column(Float())
    status: Mapped[bool] = mapped_column(default=False)
    readiness: Mapped[bool] = mapped_column(default=False)
    obtaining: Mapped[bool] = mapped_column(default=False)

    user_rel: Mapped['User'] = relationship(back_populates='order_rel')
    cart_rel: Mapped['Cart'] = relationship(back_populates='order_rel')


class Collecting_the_cake(Base):

    __tablename__ = 'collecting_the_cake'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id', ondelete='CASCADE'))
    event: Mapped[str] = mapped_column(String())
    image: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    data: Mapped[str] = mapped_column(String())
    address: Mapped[str] = mapped_column(String())
    readiness: Mapped[bool] = mapped_column(default=False)
    obtaining: Mapped[bool] = mapped_column(default=False)

    user_rel: Mapped['User'] = relationship(back_populates='collecting_rel')
    cart_rel: Mapped['Cart'] = relationship(back_populates='collecting_rel')

async def async_main():
    async with create_engine(config).begin() as conn:
        await conn.run_sync(Base.metadata.create_all)