import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    login: str = Field(..., env="LOGIN")
    password: str = Field(..., env="PASSWORD")
    domain: str = Field(..., env="DOMAIN")
    smtp_host: str = Field(..., env="SMTP_HOST")
    smtp_port: str = Field(..., env="SMTP_PORT")
    ampq_url: str = Field(..., env="AMQP_URL")

    class Config:
        env_file = ".env"


TEMPLATES_DIR = "templates/"
EVENT_TO_TEMPLATE = {
    "registration": os.path.join(TEMPLATES_DIR, "mail.html"),
    "NEW_FILMS": os.path.join(TEMPLATES_DIR, "new_film.html"),
}

DATA_TO_TEMPLATE = {
    "registration": {
        "title": "Новое письмо!",
        "text": "Произошло что-то интересное! :)",
        "image": "https://pictures.s3.yandex.net:443/resources/news_1682073799.jpeg",
    },
    "NEW_FILMS": {
        "title": "Новое письмо!",
        "text": "Произошло что-то интересное! :)",
        "image": "https://pictures.s3.yandex.net:443/resources/news_1682073799.jpeg",
    },
}

settings = Settings()

EMAIL = f"{settings.login}@{settings.domain}"
