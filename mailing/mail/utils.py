import datetime

from django_celery_beat.models import PeriodicTask, IntervalSchedule


def create_task_message_send():
    schedule, created_interval = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )
    PeriodicTask.objects.create(
        interval=schedule,
        name="send_message_task",
        task="mail.send_message_task",
        enabled=True
    )
