import datetime
from typing import Union

from config import celery_app
from mailing.mail.service.send_mail import send_message
from django_celery_beat.models import PeriodicTask

from mailing.mail.utils import local_tz, utc_to_local
from logger.logger import logger


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
    """ Таска для отправки сообщений на сторонний сервис
    """
    send_message(
        message_id=message_id,
        phone=phone,
        text_message=text_message
    )


@celery_app.task(
    bind=True,
    name="mail.check_tasks_task",
    default_retry_delay=1 * 10,
    max_retries=30,
    soft_time_limit=60 * 30,
    time_limit=60 * 30,
)
def check_tasks_task(self):
    """ Таска, которая удаляет не нужные таски для рассылки
    """
    tasks = PeriodicTask.objects.all()
    date = datetime.datetime.now(local_tz)

    for task in tasks:
        if task.expires is not None:
            task_expires = utc_to_local(task.expires)
            if date > task_expires:
                task.delete()
                logger.info(f"Task - {task} deleted..")



