import asyncio
import logging


from app.config_loader import load_config
from app.database.database import create_engine_db, create_sessionmaker
from app.database.factory_table import create_all_tables
from app.main_factory import create_bot, create_dispather


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Staring bot')
    
    config = load_config()
    engine = create_engine_db(config.db)
    pool = create_sessionmaker(engine)
    await create_all_tables(engine)
    bot = create_bot(config) 

    
    dp = create_dispather(
        pool=pool
    )

    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    try:
        asyncio.run(main())
        logger.info('Запуск бота')
    except KeyboardInterrupt as exxit:
        logger.info(f'Бот закрыт {exxit}')
