from typing import Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from core.schemas.dtos import BaseSchema

from .base_schema_for_event import BaseSchemaForEvent
from typing import Literal, Optional
from pydantic import BaseModel
from core.logger import AppLogger
from .rabbit_base import RabbitBase


async def do_something(message: dict) -> None:
    pass


class RabbitControllerBase:
    """
    Общая реализация контроллера.
    Кролик инициализирует событие в обменник и слушает через одну очередь события от другого сервиса.
    Текущая реализация - контроллер может прослушивать только один обменник через спец. очередь для этого.
    """
    def __init__(self, rabbit: RabbitBase):
        self.rabbit = rabbit
        self.exchange_to_send_own_event = None
        self.queue_for_listening_events_from_another_one_service = None
        self.exchange_name_to_send_own_event = ''  # переопределить в наследнике
        self.queue_and_exchange_event_schema = BaseSchemaForEvent()  # переопределить в наследнике

    async def init(self):
        """
        Метод инициализации всех очередей и обменников внутри контроллера для конкретного сервиса.
        У каждого сервиса набор и названия очередей/обменников свой.
        """
        try:
            """
            пока так, т.к. не продумана логика явного ожидания поднятия сервиса, где объявляется обменник (обменника 
            может не быть, а очередь к нему подвязывается)
            эта проблема может быть легко решена путем создания сущности обменника в самом контроллере с целью только
            привязки очереди к обменнику, без использования контроллером обменника напрямую.
            """
            if not self.queue_for_listening_events_from_another_one_service:
                self.queue_for_listening_events_from_another_one_service = await self.rabbit.declare_queue(
                    queue_name=self.queue_and_exchange_event_schema.queue,
                    exchange_name=self.queue_and_exchange_event_schema.depends_on_exchange)
        except Exception as e:
            AppLogger.error(e.__str__())
            await self.rabbit.reconnect_channel()

        if not self.exchange_to_send_own_event:
            self.exchange_to_send_own_event = await self.rabbit.declare_exchange(
                exchange_name=self.exchange_name_to_send_own_event
            )

    async def consume_queue_for_events_from_another_service(self) -> None:
        """
        Метод - пример как настроить прослушку с внешнего сервиса ивентов.
        Очередь принадлежит этому сервису, а обменник общий, деклалирутеся очередь и ее связь с обменником.
        На каждый ивент нужна своя очередь в контроллере потребителя и отдельный метод прослушивания.
        """
        await self.init()
        await self.rabbit.consume_queue(
            queue_instance=self.queue_for_listening_events_from_another_one_service,
            do_something=self.queue_and_exchange_event_schema.function
        )

    async def publish_new_own_event(
            self,
            data_schema: BaseModel,
            routing_key: str = 'info',
            convert_data_type: Optional[Literal['json']] = None
    ) -> None:
        """
        Метод публикации сообщения в обменник.
        :param exchange_name: имя обменника.
        :param routing_key: строковый тип подписки на обменник.
        :param data_schema: заполненные данные в виде схемы pydantic для отправки.
        :param convert_data_type: тип конвертации данных.
        :return: ничего.
        """
        async with self.rabbit.rabbitmq_async_connection:
            if not self.exchange_to_send_own_event:
                await self.init()

            to_send = self.rabbit.convert_data_to_message_sending_type(data_schema, convert_data_type)
            await self.exchange_to_send_own_event.publish(to_send, routing_key=routing_key)
