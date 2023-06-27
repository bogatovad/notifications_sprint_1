
from aio_pika import connect, Message
import orjson

from core.config import settings
from models.events import RequestEventModel, ResponseModel, UserModel


class RabbitPublisher:
    def __init__(self):
        self._connection = None
        self._channel = None
        self._exchange = None

    async def connect(self) -> None:
        self._connection = await connect(settings.rabbit_connection)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(settings.rabbitmq_exchange)

    async def create_exchange(self, exchange_name: str):
        self.exchange = await self._channel.declare_exchange(name=exchange_name)

    async def disconnect(self) -> None:
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        self._connection = None
        self._channel = None


    async def send_message(self, queue_name: str, message_data: ResponseModel):
        message = Message(
            body=orjson.dumps(message_data.dict()),
            delivery_mode=settings.rabbitmq_delivery_mode
        )
        queue = await self._channel.declare_queue(name=queue_name, durable=True)
        await queue.bind(self._exchange)
        await self._exchange.publish(
            routing_key=queue_name,
            message=message
        )

    def close(self):
        self._connection.close()


class RabbitWorker(RabbitPublisher):
    @staticmethod
    def _get_data(event, user):
        event.context["username"] = user.username
        return ResponseModel(
            event_type=event.event_name, email=user.email, context=event.context
        )

    async def produce(self, event: RequestEventModel, user: UserModel):
        response_data = self._get_data(event, user)
        await self.send_message(queue_name=f"email.{event.event_type}", message_data=response_data)

    async def produce_many(self, event: RequestEventModel, user_list: list[UserModel]):
        for user in user_list:
            response_data = self._get_data(event, user)
            await self.send_message(
                queue_name=f"email.{event.event_type}", message=response_data
            )


rabbitmq_worker: RabbitWorker = RabbitWorker()


def get_rabbitmq() -> RabbitWorker:
    return rabbitmq_worker
