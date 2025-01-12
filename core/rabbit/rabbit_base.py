from json import dumps, loads
from typing import Awaitable
from typing import Callable
from typing import Optional

from aio_pika import Channel
from aio_pika import DeliveryMode
from aio_pika import ExchangeType
from aio_pika import Message
from aio_pika import connect
from aio_pika.abc import AbstractExchange
from aio_pika.abc import AbstractIncomingMessage
from aio_pika.abc import AbstractQueue
from aio_pika.channel import Queue
from core.logger import AppLogger
from pydantic import BaseModel

from core.settings import common_settings
from .common import create_rabbit_channel


class RabbitBase:
    """Класс асинхронного рэббита, прослушивающий очереди и отправляющий ответы"""

    def __init__(
            self,
            connection: connect,
            ch: Channel
    ):
        self.rabbitmq_async_connection = connection
        self.channel = ch

    async def reconnect_channel(self) -> None:
        """
        Метод позволяет переподключить канал после того, как было вызвано исключение при работе с репозиторием кролика.
        Решает проблему aiormq.exceptions.ChannelInvalidStateError: Channel closed by RPC timeout.
        Метод вызывается в контроллере.
        """
        self.channel = await create_rabbit_channel(self.rabbitmq_async_connection)

    @staticmethod
    async def consume_queue(queue_instance: Queue, do_something: Callable[[dict], Awaitable[None]]) -> None:
        """
        Метод прослушивания очереди не колбэком. Для каждой очереди нужно вызывать метод индивидуально, что
        реализовано в контроллере.
        :param queue_instance: задекларированная очередь.
        :param do_something: асинхронная функция (контроллер) обработки сообщения.
        :return: ничего.
        """
        async with queue_instance.iterator() as iterator:
            message: AbstractIncomingMessage
            async for message in iterator:
                try:
                    async with message.process(ignore_processed=True):  # не делать ничего если сообщение уже обработано
                        message_ = loads(loads(message.body.decode()))
                        await do_something(message_)
                        await message.ack()

                except Exception as error:
                    AppLogger.error(repr(error))
                    # await self.publish_to_logging_queue(message, repr(error))

    async def declare_exchange(self, exchange_name: str) -> AbstractExchange:
        """
        Метод создает обменник.
        :return: обменник.
        """
        return await self.channel.declare_exchange(exchange_name, ExchangeType.FANOUT)

    async def declare_queue(self, queue_name: str, exchange_name: Optional[str] = None) -> AbstractQueue:
        """
        Метод создает и привязывает очереди к обменнику, если она есть, если нет, то просто создается очередь.
        :param queue_name: имя очереди.
        :param exchange_name: имя обменника, его может не быть и тогда не будет привязки к обменнику.
        :return: очередь.
        """
        queue = await self.channel.declare_queue(name=queue_name, durable=False)
        if exchange_name:
            await queue.bind(exchange_name)
        return queue

    async def publish_to_logging_queue(self, mess_obj, error_info) -> None:
        """
        Текущая версия метода публикации ошибок в очередь для логов.
        :param mess_obj: поступившее сообщение
        :param error_info: словарь с парамтерами об ошибке
        :return:
        """
        AppLogger.error(repr(error_info))
        await mess_obj.ack()
        await self.channel.default_exchange.publish(
            Message(
                dumps(error_info).encode('utf-8'),
                delivery_mode=DeliveryMode.NOT_PERSISTENT
            ),
            routing_key=common_settings.LOGGING_QUEUE_NAME
        )

    def convert_data_to_message_sending_type(self, data_schema: BaseModel, convert_data_type: str) -> Message:
        """
        Метод конвертации данных в необходимый формат для передачи через aio_pika.IncomingMessage.
        На данный момент реализован для json, остальные типы будут добавляться по необходимости.
        :param data_schema: pydantic модель с данными
        :param convert_data_type: тип в который нужно конвертировать
        :return: закодированное сообщение в байтах.
        :exception: NotImplementedError в случаях, когда метод вызывается с нереализованным типом конвертации данных.
        """
        if convert_data_type == 'json':
            to_send = data_schema.json()
            to_send = dumps(to_send).encode('utf-8')
            return Message(to_send, delivery_mode=DeliveryMode.PERSISTENT)

        raise NotImplementedError
