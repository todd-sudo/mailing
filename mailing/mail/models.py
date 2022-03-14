from django.db import models


class MailingList(models.Model):
    """ Рассылка
    """
    external_id = models.UUIDField("Уникальный ID", unique=True)
    date_start = models.DateTimeField("Время запуска")
    text = models.TextField(
        "Текст сообщений",
        max_length=500,
        null=True,
        blank=True
    )
    date_stop = models.DateTimeField(
        "Время окончания", )

    def __str__(self):
        return f"{self.external_id}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class Client(models.Model):
    """ Клиент
    """
    external_id = models.UUIDField("Уникальный ID", unique=True)
    phone = models.PositiveBigIntegerField("Телефон")
    operator_code = models.PositiveIntegerField(
        "Код оператора",
        null=True,
        blank=True
    )
    tag = models.CharField("Тег", max_length=100, null=True, blank=True)
    timezone = models.CharField(
        "Часовой пояс",
        default="UTC",
        max_length=30,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.external_id}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Message(models.Model):
    """ Сообщение
    """
    external_id = models.UUIDField("Уникальный ID", unique=True)
    create_at = models.DateTimeField(
        "Время создания сообщения",
        auto_now_add=True,
    )
    status = models.BooleanField("Статус отправки", default=False)
    mailing_list = models.ForeignKey(
        MailingList,
        on_delete=models.CASCADE,
        verbose_name="Рассылка",
        related_name="messages",
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="Клиент",
        related_name="messages",
    )

    def __str__(self):
        return f"{self.external_id}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
