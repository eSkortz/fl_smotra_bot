from pydantic_settings import BaseSettings
from pydantic import SecretStr


class AppConfig(BaseSettings):
    DATABASE_IP: SecretStr
    DATABASE_NAME: SecretStr
    DATABASE_LOGIN: SecretStr
    DATABASE_PASSWORD: SecretStr
    TELEGRAM_TOKEN: SecretStr
    ADMIN_DISCORD_TOKEN: SecretStr

    # class Config:
    #     env_file = 'temp/.env'
    #     env_file_encoding = 'utf-8'


app_config = AppConfig()
