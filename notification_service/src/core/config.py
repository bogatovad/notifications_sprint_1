from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = Field("notification_service", env="PROJECT_NAME")
    host: str = Field("notification_api", env="NS_HOST")
    port: int = Field(8080, env="NS_PORT")
    rabbitmq_host: str = Field('rabbitmq', env="RABBITMQ_HOST")
    rabbitmq_port: int = Field(5672, env="RABBITMQ_PORT")
    rabbitmq_user: str = Field('rmuser', env="RABBITMQ_USER")
    rabbitmq_password: str = Field(env="RABBITMQ_PASSWORD")

    class Config:
        env_file = "envs/.env"


settings = Settings()
