import pika
import json

from core.config import settings
from models.events import ResponseModel, RequestEventModel, UserModel


class RabbitPublisher:
    def __init__(self, rabbitmq_host: str, rabbitmq_port: int):
        self.credentials = pika.PlainCredentials(settings.rabbitmq_user, settings.rabbitmq_password)
        self.host=rabbitmq_host
        self.port=rabbitmq_port
        self.connection = None

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, 
                                                                             port=self.port,
                                                                             credentials=self.credentials))
        self.channel = self.connection.channel()
        
    def send_message(self, queue_name: str, message: ResponseModel):
        message = json.dumps({'message': message})
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode= settings.rabbitmq_delivery_mode))

    def close(self):
        self.connection.close()


class RabbitWorker(RabbitPublisher):

    @staticmethod
    def _get_data(event, user):
        template_context = event.context['username'] = user.login
        return ResponseModel(
        event_name=event.event_name,
        email=user.email,
        context=template_context
        )

    def produce(self, event: RequestEventModel, user: UserModel):
        response_data = self._get_data(event, user)
        self.send_message(queue_name=f'email.{event.event_type}', message=response_data)

    def produce_many(self, event: RequestEventModel, user_list: list[UserModel]):
        for user in user_list:
            response_data = self._get_data(event, user)
            self.send_message(queue_name=f'email.{event.event_type}', message=response_data)


rabbitmq_worker: RabbitWorker = RabbitWorker(
    settings.rabbitmq_host,
    settings.rabbitmq_port
)


def get_rabbitmq() -> RabbitWorker:
    return rabbitmq_worker
