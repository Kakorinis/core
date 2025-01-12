from aio_pika import Channel
from aio_pika import connect

from core.rabbit import RabbitBase


async def create_rabbit_async_instance(
        connection: connect,
        ch: Channel
) -> RabbitBase:
    """
    Фабричная функция создания экземпляра Rabbit.
    Была среди остальных 2 функций в depends.py, но выведен отдельно из-за циклического импорта.
    Подается в контейнер.
    """

    rabbit = RabbitBase(connection=connection, ch=ch)
    return rabbit
