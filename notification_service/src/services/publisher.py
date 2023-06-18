import pika
import json
import time

from core.config import settings


class RabbitPublisher:
    def __init__(self, rabbitmq_host, rabbitmq_port):
        self.credentials = pika.PlainCredentials(settings.rabbitmq_user, settings.rabbitmq_password)
        self.host=rabbitmq_host
        self.port=rabbitmq_port
        self.connection = None

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, 
                                                                             port=self.port,
                                                                             credentials=self.credentials))
        self.channel = self.connection.channel()
        
    def send_message(self, queue_name, message):
        message = json.dumps({'message': message})
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2))

    def close(self):
        self.connection.close()


rabbitmq_broker: RabbitPublisher = RabbitPublisher(
    settings.rabbitmq_host,
    settings.rabbitmq_port
)


def get_rabbitmq() -> RabbitPublisher:
    """Function required for dependency injection"""
    return rabbitmq_broker
