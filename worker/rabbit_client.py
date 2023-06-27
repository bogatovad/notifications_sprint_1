import pika
from names_queue import NEW_FILMS_QUEUE, SEND_WELCOME_QUEUE
from settings import settings
from tasks import send


class RabbitMq:
    """Класс для взаимодействия с очередью сообщений."""

    def __init__(self) -> None:
        self.credentials = pika.PlainCredentials(settings.rm_user, settings.rm_password)
        self.connect = pika.SelectConnection(
            parameters=pika.ConnectionParameters(
                host=settings.rabbit_host,
                port=settings.rabbit_port,
                credentials=self.credentials,
            ),
            on_open_callback=self._on_open,
        )

    def run(self) -> None:
        try:
            self.connect.ioloop.start()
        except KeyboardInterrupt:
            self.connect.close()

    def _on_channel_open(self, channel) -> None:
        for queue in (SEND_WELCOME_QUEUE, NEW_FILMS_QUEUE):
            channel.exchange_declare(
                exchange='main',
                exchange_type='direct',
                durable=True,
                auto_delete=False
            )
            channel.basic_consume(queue=queue, on_message_callback=self._callback)

    def _on_open(self, connection) -> None:
        connection.channel(on_open_callback=self._on_channel_open)

    @staticmethod
    def _callback(channel, method, properties, body) -> None:
        send.delay(body)
        channel.basic_ack(delivery_tag=method.delivery_tag)
