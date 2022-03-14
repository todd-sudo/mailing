from django_celery_beat.models import PeriodicTask, IntervalSchedule


def create_task_create_category_poi(apps, schema_editor):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,

    )
    PeriodicTask.objects.create(
        interval=schedule,
        name="create_category_poi",
        task="tom_tom.task_create_category_poi",
        enabled=False,
    )

