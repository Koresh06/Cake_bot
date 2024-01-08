import asyncio
import os

from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher
from app.handlers.user_handler import router
from app.handlers.admin_handler import admin
from app.handlers.order_placement import payment
from app.handlers.cake_assembly import cake
from app.handlers.product_cards import card
from app.handlers.basket_user import basket
from app.handlers.order_user import order
from app.database.models import async_main


load_dotenv(find_dotenv())

async def main():
    await async_main() #Запуск БД
    bot: Bot = Bot(token=os.getenv('TOKEN'), parse_mode='HTML')
    dp: Dispatcher = Dispatcher()
    
    dp.include_routers(
        order,
        basket,
        card,
        cake,
        payment,
        admin, 
        router,
    )
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    try:
        print('Бот запущен!')
        asyncio.run(main())
    except KeyboardInterrupt as exx:
        print(exit())