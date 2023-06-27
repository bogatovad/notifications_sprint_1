from http import HTTPStatus

from fastapi import APIRouter, Depends

from models.events import RequestEventModel
from services.publisher import RabbitWorker, get_rabbitmq
from services.user_service import UserService, get_user_service

router = APIRouter()


@router.post("/send-notification/email")
async def send_notifications(
    event: RequestEventModel,
    rabbit_worker: RabbitWorker = Depends(get_rabbitmq),
    user_service: UserService = Depends(get_user_service),
):
    if event.type == "personal":
        user = await user_service.find_one(id=event.receiver)
        await rabbit_worker.produce(event, user)
    else:
        user_list = await user_service.get_users(event.receiver)
        await rabbit_worker.produce_many(event, user_list)
    return HTTPStatus.ACCEPTED
