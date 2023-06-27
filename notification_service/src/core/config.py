from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = Field("notification_service", env="PROJECT_NAME")
    host: str = Field("notification_api", env="NS_HOST")
    port: int = Field(8080, env="NS_PORT")

    db_name: str = Field("postgres", env="DB_NAME")
    pg_user: str = Field("app", env="POSTGRES_USER")
    pg_password: str = Field("123qwe", env="POSTGRES_PASSWORD")
    pg_host: str = Field("notifications_db", env="POSTGRES_HOST")
    pg_port: int = Field(5432, env="POSTGRES_PORT")

    rabbitmq_host: str = Field("rabbitmq", env="RABBITMQ_HOST")
    rabbitmq_port: int = Field(5672, env="RABBITMQ_PORT")
    rabbitmq_user: str = Field("rmuser", env="RABBITMQ_USER")
    rabbitmq_password: str = Field(env="RABBITMQ_PASSWORD")
    rabbitmq_delivery_mode: int = Field(2, env="RABBITMQ_DELIVERY_MODE")
    rabbitmq_exchange: str = Field("main", env="RABBITMQ_EXCHANGE")

    class Config:
        env_file = "envs/.env"

    @property
    def db_uri(self):
        """Возвращает URI базы данных."""
        return f"postgresql://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.db_name}"

    @property
    def rabbit_connection(self):
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}/"


settings = Settings()
