import asyncio
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config_loader import create_config_from_toml
from aiogram import Bot, Dispatcher
from app.handlers.user_handler import router
from app.handlers.admin_handler import admin
from app.handlers.order_placement import payment
from app.handlers.cake_assembly import cake
from app.handlers.product_cards import card
from app.handlers.basket_user import basket
from app.handlers.order_user import order
from app.database.models import async_main


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Staring bot')
    
    await async_main() #Запуск БД
    config = create_config_from_toml('/config/config.template.toml') #Создание конфига
    async_session = async_sessionmaker(create_engine(config)) #Создание сессии

    bot: Bot = Bot(token=create_config_from_toml('/config/config.template.toml').bot.token, parse_mode='HTML')
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
        asyncio.run(main())
        logger.info('Запуск бота')
    except KeyboardInterrupt as exxit:
        logger.info(f'Бот закрыт {exxit}')
