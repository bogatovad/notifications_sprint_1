from clickhouse_driver import Client


def init_ch_connection():
    return Client(host="clickhouse-node1")


def init_clickhouse_db(client):
    client.execute(
        f"CREATE DATABASE IF NOT EXISTS notification",
    )
