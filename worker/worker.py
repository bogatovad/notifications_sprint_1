import pika
from clickhouse_driver import Client
from notification_store import init_ch_connection, init_clickhouse_db
from tasks import send


def connect_to_pika(on_open):
    """Подключение к rabbitmq."""
    credentials = pika.PlainCredentials("rmuser", "rmpassword")
    return pika.SelectConnection(
        parameters=pika.ConnectionParameters(
            host="rabbitmq_service", port=5672, credentials=credentials
        ),
        on_open_callback=on_open,
    )


def main():
    ch_client = init_ch_connection()
    init_clickhouse_db(ch_client)
    ch_client.execute("SET allow_experimental_object_type=1;")
    ch_client.execute(
        "CREATE TABLE IF NOT EXISTS notification.regular_table (id String, status String, context String) Engine=MergeTree() ORDER BY id"
    )

    def on_channel_open(channel):
        channel.basic_consume(queue="hello", on_message_callback=callback)
        channel.basic_consume(queue="hello", on_message_callback=callback)

    def on_open(connection):
        connection.channel(on_open_callback=on_channel_open)

    def callback(channel, method, properties, body):
        send.delay(body)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    connect = connect_to_pika(on_open)
    try:
        connect.ioloop.start()
    except KeyboardInterrupt:
        connect.close()


main()
