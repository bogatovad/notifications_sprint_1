from django.db import models


class StatusChoice(models.TextChoices):
    SENT = 'sent', 'Отправлено'
    PENDING = 'pending', 'В процессе'
    FAILED = 'failed', 'Не отправлено'
