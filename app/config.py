from dataclasses import dataclass


@dataclass
class BotConfig:
    token: str

@dataclass
class DbConfig:
    type: str | None = None
    connector: str | None = None
    host: str | None = None
    port: int | None = None
    login: str | None = None
    password: str | None = None
    name: str | None = None
    path: str | None = None
    echo: bool = False

    @property
    def uri(self):
        if self.type in ("mysql", "postgresql"):
            url = (
                f"{self.type}+{self.connector}://"
                f"{self.login}:{self.password}"
                f"@{self.host}:{self.port}/{self.name}"
            )
        elif self.type == "sqlite":
            url = f"{self.type}+aiosqlite:///{self.path}"
        else:
            raise ValueError("DB_TYPE not mysql, sqlite or postgres")
        return url

@dataclass
class Config:
    bot: BotConfig
    db: DbConfig