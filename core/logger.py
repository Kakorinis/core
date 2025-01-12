from logging import DEBUG
from logging import Logger
from logging import getLogger
from logging.config import dictConfig
from typing import Optional


class AppLogger:
    """
    Логгер.
    """

    # Настройки логирования
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            # 'default': {
            #     '()': 'ecs_logging.StdlibFormatter',
            # },
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
        },
        'loggers': {
            'uvicorn.error': {
                'level': 'INFO',
                'handlers': [
                    'default',
                ],
            },
            'uvicorn.access': {
                'handlers': [
                    'default',
                ],
                'level': 'INFO',
                'propagate': False,
            },
            'app': {
                'handlers': [
                    'default',
                ],
                'level': 'INFO',
                'propagate': True
            },
        },
    }
    app_logger: Optional[Logger] = None

    @classmethod
    def init(cls, is_debug: bool = False) -> None:
        """
        Инициализация логгера.

        :param is_debug: Режим отладки.
        :return: None.
        """
        dictConfig(cls.LOGGING_CONFIG)
        cls.app_logger = getLogger('app')
        if is_debug:
            cls.app_logger.setLevel(DEBUG)
        getLogger('sqlalchemy.engine.Engine').disabled = not is_debug

    @classmethod
    def debug(cls, message: str) -> None:
        """
        Логирование отладочных сообщений.

        :param message: Сообщение.
        :return: None.
        """
        if cls.app_logger:
            cls.app_logger.debug(message)

    @classmethod
    def info(cls, message: str) -> None:
        """
        Логирование информационных сообщений.

        :param message: Сообщение.
        :return: None.
        """
        cls.app_logger.info(message)

    @classmethod
    def warning(cls, message: str) -> None:
        """
        Логирование предупреждений.

        :param message: Сообщение.
        :return: None.
        """
        cls.app_logger.warning(message)

    @classmethod
    def error(cls, message: str) -> None:
        """
        Логирование ошибок.

        :param message: Сообщение.
        :return: None.
        """
        cls.app_logger.error(message)
