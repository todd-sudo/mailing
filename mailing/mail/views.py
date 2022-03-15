import datetime
import uuid

from rest_framework import generics, status
from django.db.models import Q
from rest_framework.response import Response

from .models import Client, Message, MailingList
from .serializers import (
    ClientCreateUpdateSerializer,
    MailingCreateUpdateSerializer,
    ClientSerializer,
    MailingDetailSerializer,
)
from .utils import create_task_message_send, utc_to_local
from logger.logger import logger


# Client
class CreateClientView(generics.CreateAPIView):
    """ Создание клиента
    """
    queryset = Client.objects.all()
    serializer_class = ClientCreateUpdateSerializer


class UpdateClientView(generics.UpdateAPIView):
    """ Обновление данных клинта
    """
    queryset = Client.objects.all()
    serializer_class = ClientCreateUpdateSerializer
    lookup_field = "id"


class DestroyClientView(generics.DestroyAPIView):
    """ Удаление данных клиента
    """
    queryset = Client.objects.all()
    lookup_field = "id"


# MailingList
class MailingCreateView(generics.CreateAPIView):
    """ Создание рассылки
    """
    serializer_class = MailingCreateUpdateSerializer
    queryset = MailingList.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        mail_external_id = dict(serializer.data).get("external_id")
        ml = MailingList.objects.get(external_id=mail_external_id)

        date_start = utc_to_local(ml.date_start)
        date_stop = utc_to_local(ml.date_stop)

        clients = Client.objects.filter(
            Q(tag=ml.tag) | Q(operator_code=ml.operator_code)
        )
        logger.info(f"Рассылка: {ml.external_id}|Клиентов: {len(clients)}")

        new_message = Message.objects.create(
            external_id=uuid.uuid4(),
            create_at=datetime.datetime.now(),
            status=True,
            mailing_list=ml,
        )
        logger.info(f"Сообщение: {new_message} создано")
        new_message.clients.add(*clients)

        tasks = []
        for client in clients:
            task = create_task_message_send(
                name_task=f"task_{uuid.uuid4().hex}",
                text_message=ml.text,
                message_id=new_message.pk,
                phone=int(client.phone),
                start_time=date_start,
                expires=date_stop,
            )
            logger.info(f"Задача: {task} создана")
            tasks.append(task)
        logger.info(f"Всего задач: {len(tasks)}")
        if tasks:
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        logger.error(
            "Рассылка не запущена, нет клиентов, попадающих под фильтры"
        )
        return Response(
            {
                "detail": "рассылка не запущена, нет клиентов, "
                          "попадающих под фильтры"
            },
            status=status.HTTP_400_BAD_REQUEST,
            headers=headers
        )


class MailingUpdateView(generics.UpdateAPIView):
    """ Обновление рассылки
    """
    queryset = MailingList.objects.all()
    serializer_class = MailingCreateUpdateSerializer
    lookup_field = "id"


class MailingDestroyView(generics.DestroyAPIView):
    """ Удаление рассылки
    """
    queryset = MailingList.objects.all()
    lookup_field = "id"


class MailingListClientsListView(generics.ListAPIView):
    """ Список клиентов одной рассылки
    """
    lookup_field = "id"
    serializer_class = ClientSerializer

    def get_queryset(self):
        ml = MailingList.objects.get(id=self.kwargs[self.lookup_field])
        clients = Client.objects.filter(messages__mailing_list=ml)
        return clients


class MailingListView(generics.ListAPIView):
    """ Просмотр списка рассылок
    """
    serializer_class = MailingCreateUpdateSerializer

    def get_queryset(self):
        queryset = MailingList.objects.all()
        return queryset


class MailingDetailView(generics.RetrieveAPIView):
    """ Просмотр детальной информации о рассылке
    """
    serializer_class = MailingDetailSerializer
    lookup_field = "id"
    queryset = MailingList.objects.all()
