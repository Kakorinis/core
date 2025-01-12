from aio_pika import Channel
from aio_pika import connect


async def create_rabbit_connection(url: str) -> connect:
    """Фабричная функция создания подключения к RabbitMQ"""

    return await connect(url)


async def create_rabbit_channel(connection: connect) -> Channel:
    """Фабричная функция создания канала для имеющегося подключения к RabbitMQ"""

    ch = await connection.channel()
    await ch.set_qos(prefetch_count=1)
    return ch
