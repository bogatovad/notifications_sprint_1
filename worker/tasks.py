import os
import smtplib
import uuid
from email.message import EmailMessage

from celery import Celery
from exceptions import TemplateNotExist
from jinja2 import Environment, FileSystemLoader
from notification_store import init_ch_connection
from settings import DATA_TO_TEMPLATE, EMAIL, EVENT_TO_TEMPLATE, settings

from enums import STATUS
import json


broker_url = "amqp://rmuser:rmpassword@rabbitmq_service"
redis_url = "redis://redis"
app = Celery("tasks", broker=redis_url, backend=redis_url)


def create_base_message():
    """Создание основы для сообщения."""
    message = EmailMessage()

    message["From"] = EMAIL
    message["To"] = ",".join([EMAIL])
    message["Subject"] = "Привет!"

    return message


def render_template(message_dict):
    """Генерация шаблона для отправки письма."""
    current_path = os.path.dirname(__file__)
    loader = FileSystemLoader(current_path)
    env = Environment(loader=loader)

    event = message_dict.get("event")

    if event not in EVENT_TO_TEMPLATE or event not in DATA_TO_TEMPLATE:
        raise TemplateNotExist

    template = env.get_template(EVENT_TO_TEMPLATE[event])
    return template.render(**DATA_TO_TEMPLATE[event])


def init_smtp():
    """Инициализация smtp сервера."""
    server = smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port)
    server.login(settings.login, settings.password)

    return server


# def save_notification(data_message: dict[str, str]) -> None:
#     """Сохранение уведомления в базу."""
#     ch_client = init_ch_connection()
#     template_query: str = (
#         "INSERT INTO notification.regular_table "
#         "(id, status, context, date) VALUES ('{id}', '{status}', '{context}')"
#     )
#     query = template_query.format(**data_message)
#     ch_client.execute(query)


def send_message(email, message):
    """Функция для отправки сообщения."""
    server = init_smtp()
    message = message.as_string()

    try:
        server.sendmail(EMAIL, [email], message)
    except smtplib.SMTPException:
        status = STATUS.FAIL.value
    else:
        status = STATUS.SUCCESS.value
    finally:
        data_message: dict[str, str] = {
            "id": str(uuid.uuid4()),
            "status": status,
            "context": message,
        }

        # Сохраняем данные в clickhouse.
        # save_notification(data_message)
        server.close()


@app.task
def send(body):
    """Таска для отправки сообщения."""
    message = body.decode("utf-8")
    message_dict = json.loads(message)
    output = render_template(message_dict)
    message = create_base_message()
    message.add_alternative(output, subtype="html")

    email = message_dict.get("email")
    send_message(email, message)
