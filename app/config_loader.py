import toml

from app.config import BotConfig, Config, DbConfig


def load_config() -> Config:
    config_data = toml.load('config\config.template.toml')
    bot_config_data = config_data.get('bot', {})
    db_config_data = config_data.get('database', {})
    
    bot_config = BotConfig(token=bot_config_data.get('token', ''))
    db_config = DbConfig(type=db_config_data.get('type', ''), path=db_config_data.get('path', ''), echo=db_config_data.get('echo', False))

    return Config(bot=bot_config, db=db_config)