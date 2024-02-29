from dataclasses import dataclass

@dataclass
class BotConfig:
    token: str

@dataclass
class DbConfig:
    path: str
    echo: bool

@dataclass
class Config:
    bot: BotConfig
    db: DbConfig