import datetime
import time
from typing import Union

from config import celery_app
from mailing.mail.service.send_mail import send_message
from mailing.mail.utils import create_task_message_send


@celery_app.task(
    bind=True,
    name="mail.send_message_task",
    default_retry_delay=1 * 10,
    max_retries=30,
    soft_time_limit=60 * 30,
    time_limit=60 * 30,
)
def send_message_task(
        self,
        message_id: int,
        phone: Union[int, str],
        text_message: str
):
    response = send_message(
        message_id=message_id,
        phone=phone,
        text_message=text_message
    )
    if response.status_code == 200:
        print(f"is task status code {response.status_code}")

