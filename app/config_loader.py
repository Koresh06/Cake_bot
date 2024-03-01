import toml
from typing import Union

from cakes_to_order.app.config import DbConfig, BotConfig


def load_config_from_toml(file_path: str, config_type: Union[BotConfig, DbConfig]) -> Union[BotConfig, DbConfig]:
    """Load TOML file and create config object."""
    with open(file_path, "r") as file:
        config_dict = toml.load(file)
    
    if config_type == BotConfig:
        return BotConfig(token=config_dict.get("bot", {}).get("token", ""))
    elif config_type == DbConfig:
        db_config = config_dict.get("db", {})
        return DbConfig(
            path=db_config.get("path", ""),
            echo=db_config.get("echo", False)
        )
    else:
        raise ValueError("Invalid config type")