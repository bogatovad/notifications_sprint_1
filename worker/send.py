import pika
from names_queue import SEND_WELCOME_QUEUE

credentials = pika.PlainCredentials("rmuser", "rmpassword")
rmq_connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="rabbitmq", port=5672, credentials=credentials)
)

rmq_channel_new_film = rmq_connection.channel()
rmq_channel_new_film.queue_declare(queue=SEND_WELCOME_QUEUE, durable=True)
res = rmq_channel_new_film.basic_publish(
    exchange="",
    routing_key=SEND_WELCOME_QUEUE,
    body=b'{"email": "artembbogatov@yandex.ru", "context": '
    b'{"title": "privet", "text": "privet"}, "event":"registration"}',
    properties=pika.BasicProperties(delivery_mode=2),
)
print(res)
