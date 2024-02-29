from ast import Dict
import toml
from app.config import Config, BotConfig, DbConfig


def load_toml_file(file_path: str) -> Dict:
    """Load TOML file and return as dictionary."""
    with open(file_path, "r") as file:
        config_dict = toml.load(file)
    return config_dict

def create_bot_config(config_dict: Dict) -> BotConfig:
    """Create BotConfig object from dictionary."""
    bot_config = config_dict.get("bot", {})
    return BotConfig(token=bot_config.get("token", ""))

def create_db_config(config_dict: Dict) -> DbConfig:
    """Create DbConfig object from dictionary."""
    db_config = config_dict.get("db", {})
    return DbConfig(
        path=db_config.get("path", ""),
        echo=db_config.get("echo", False)
    )

def create_config_from_toml(file_path: str) -> Config:
    """Create Config object from TOML file."""
    config_dict = load_toml_file(file_path)
    bot_config = create_bot_config(config_dict)
    db_config = create_db_config(config_dict)
    return Config(bot=bot_config, db=db_config)