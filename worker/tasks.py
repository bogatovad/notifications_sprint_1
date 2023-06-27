import os
from celery import Celery
from exceptions import TemplateNotExist
from jinja2 import Environment, FileSystemLoader
from settings import DATA_TO_TEMPLATE, EVENT_TO_TEMPLATE
from message_sender import SendMessageManager
import json

broker_url = "amqp://rmuser:rmpassword@rabbitmq_service"
redis_url = "redis://redis"
app = Celery("tasks", broker=redis_url, backend=redis_url)


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


@app.task
def send(body):
    """Таска для отправки сообщения."""
    message = body.decode("utf-8")
    message_dict = json.loads(message)
    html_content = render_template(message_dict)

    email = message_dict.get("email")

    manager = SendMessageManager()
    manager.send(html_content)
