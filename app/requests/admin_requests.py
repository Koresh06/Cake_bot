from app.database.models import async_session
from app.database.models import User, Product, Categories, Orders
from sqlalchemy import select, update


async def output_categories():
    async with async_session() as session:
        name_cat = await session.execute(select(Categories.name, Categories.id))
    return name_cat.all()

async def add_categories(name_cat):
    async with async_session() as session:
        name_d = await session.scalar(select(Categories).where(Categories.name == name_cat))
        if not name_d:
            session.add(Categories(name=name_cat))
            await session.commit()
            return True
        else:
            return False
        
async def add_product_db(tg_id, product: dict):
    async with async_session() as session:
        try:
            user_d = await session.scalar(select(User).where(User.tg_id == tg_id))
            session.add(Product(user_id=user_d.id, categories_id=product['id_categ'], name=product['name'],   image=product['image'], description=product   ['description'], price=product['price']))
            count = await session.scalar(select(Categories.count).where(Categories.id == product['id_categ']))
            count += 1
            await session.execute(update(Categories).where(Categories.id == product['id_categ']).values(count=count))
            await session.commit()
            return True
        except Exception as exxit:
            print(exxit)
            return False
        finally:
            session.commit()

#Подтверждение заказа
async def readiness_order(index):
    async with async_session() as session:
        if await session.execute(update(Orders).where(Orders.id == index).values(readiness=True)):
            await session.commit()
            return True
        return False
    
#Откланение заказа   
async def delete_orders(id):
    async with async_session() as session:
        try:
            order = await session.scalar(select(Orders).where(Orders.id == id))
            await session.delete(order)
            await session.commit()
            return True
        except Exception() as ex:
            print(ex)
            return False
        
#Получение списка пользователей
async def users():
    async with async_session() as session:
        users_d = await session.execute(select(User.username, User.tg_id))
        if users_d:
            return users_d.all()
        return False