import pika
from names_queue import NEW_FILMS_QUEUE


credentials = pika.PlainCredentials("rmuser", "rmpassword")
rmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", port=5672, credentials=credentials))

rmq_channel_new_film = rmq_connection.channel()
rmq_channel_new_film.queue_declare(queue='helllll', durable=True)
res = rmq_channel_new_film.basic_publish(
    exchange='', 
    routing_key='helllll',
    body=b'{"email": "artembbogatov@yandex.ru", "context": "hello", "event":"NEW_FILMS"}', 
    properties=pika.BasicProperties(delivery_mode=2)
)
print(res)