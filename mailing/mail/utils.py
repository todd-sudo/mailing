import json
from typing import Union

import pytz as pytz
from django_celery_beat.models import PeriodicTask, IntervalSchedule


def create_task_message_send(
        name_task: str,
        message_id: int,
        phone: Union[int, str],
        text_message: str,
        start_time,
        expires,
):
    schedule, created_interval = IntervalSchedule.objects.get_or_create(
        every=3,
        period=IntervalSchedule.SECONDS,
    )
    task = PeriodicTask.objects.create(
        interval=schedule,
        name=name_task,
        start_time=start_time,
        expires=expires,
        task="mail.send_message_task",
        kwargs=json.dumps({
            "message_id": message_id,
            "phone": phone,
            "text_message": text_message
        })
        # enabled=True
    )
    return task


local_tz = pytz.timezone('Europe/Moscow')


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)
