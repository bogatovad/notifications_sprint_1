from http import HTTPStatus

from fastapi import APIRouter, Depends, BackgroundTasks

from models.events import RequestEventModel
from services.publisher import RabbitPublisher, get_rabbitmq
from services.user_service import UserService, get_user_service


router = APIRouter()


def put_event_to_queue():
    pass


@router.post(
    "/send-notification/{email}"
)
async def send_notifications(
    event: RequestEventModel,
    # background_task: BackgroundTasks,
    message_service: RabbitPublisher = Depends(get_rabbitmq),
    user_service: UserService = Depends(get_user_service)
):
    queue_name = f'email.{event.name}'
    if event.type == 'single':
        message_service.send_message(queue_name, event.data)
    else:
        for user_id in event.receiver:
            message_service.send_message(queue_name, event.data)
    return HTTPStatus.OK
