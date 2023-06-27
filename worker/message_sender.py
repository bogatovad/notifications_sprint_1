import uuid

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from settings import settings
from enums import Status
from store import Store


class SendMessageManager:
    """Класс управляет рассылками по электронной почте."""
    def __init__(self) -> None:
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key['api-key'] = settings.api_key_email
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(self.configuration))
        self.store = Store()

    def send(self, html_content: str) -> bool:
        subject = "Новые фильмы"
        sender = {"name": "NotificationService", "email": "notification@yandex.ru"}
        to = [
            {"email": "ArtembBogatov@yandex.ru", "name": "Jane Doe"}
        ]
        notification_id = str(uuid.uuid4())
        status = None
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            html_content=html_content,
            sender=sender,
            subject=subject
        )
        try:
            self.api_instance.send_transac_email(send_smtp_email)
            status = Status.SUCCESS.value
        except ApiException as e:
            status = Status.FAIL.value
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
            return False

        data_clickhouse = {
            "id": notification_id,
            "status": status,
            "context": html_content
        }
        self.store.save_notification(data_clickhouse)
        return True

