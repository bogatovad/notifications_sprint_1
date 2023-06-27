from clickhouse_driver import Client
from settings import settings


class Store:
    """Класс для взаимодействия с хранилищем уведомлений."""
    def __init__(self):
        self.client = Client(host=settings.clickhouse_host)

    def create_db_notification(self):
        self.client.execute(
            f"CREATE DATABASE IF NOT EXISTS notification",
        )

    def create_table_notification(self):
        self.client.execute(
            "CREATE TABLE IF NOT EXISTS notification.regular_table "
            "(id String, status String, context String) Engine=MergeTree() ORDER BY id"
        )

    def init_db(self):
        self.create_db_notification()
        self.create_table_notification()

    def save_notification(self, data_message: dict[str, str]) -> None:
        """Сохранение уведомления в базу."""
        template_query: str = (
            "INSERT INTO notification.regular_table "
            "(id, status, context) VALUES ('{id}', '{status}', '{context}')"
        )
        self.client.execute(template_query.format(**data_message))
