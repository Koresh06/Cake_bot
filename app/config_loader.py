import toml
from typing import Union

from app.config import DbConfig, BotConfig, Config


def load_config() -> Config:
    config_data = toml.load('config\config.template.toml')
    bot_config_data = config_data.get('bot', {})
    db_config_data = config_data.get('database', {})
    
    bot_config = BotConfig(token=bot_config_data.get('token', ''))
    db_config = DbConfig(path=db_config_data.get('path', ''), echo=db_config_data.get('echo', False))

    return Config(bot=bot_config, db=db_config)