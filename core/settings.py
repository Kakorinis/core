from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class CoreSettings(BaseSettings):
    """
    Базовые настройки приложения.
    """

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # Common
    APP: str = 'main:app'
    HOST: str = '0.0.0.0'
    PORT: int = 8000
    SWAGGER_TITLE: str = 'Need to input'
    APP_VERSION: str = '0.0.0'
    ROOT_PATH: str = ''
    IS_DEBUG: bool = False
    IS_NEED_PING: bool = False  # Флаг необходимости проверки доступности требуемых сервисов

    # DB
    SQL_DSN: str = 'postgresql+asyncpg://user:pwd@localhost:port/postgres'
    SQL_SCHEMA: str = 'public'
    IS_DB_INIT_NECESSARY: bool = True  # Флаг необходимости наполнения БД значениями по умолчанию

    # rabbit
    LOGGING_QUEUE_NAME: str = 'LogQueue'


base_settings = CoreSettings()
