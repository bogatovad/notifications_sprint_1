from http import HTTPStatus

from fastapi import APIRouter, Depends, Request

from services.publisher import RabbitPublisher, get_rabbitmq


router = APIRouter()


@router.post(
    "/email_notifications"
)
async def email_notifications(
    request: Request, publisher: RabbitPublisher = Depends(get_rabbitmq)
):
    request_data = await request.json()
    queue_name = request_data['event_type']
    publisher.send_message(queue_name, request_data['data'])
    return HTTPStatus.OK
