import datetime
import pytz
import uuid


from rest_framework import generics, status
from django.db.models import Prefetch, Q
from rest_framework.response import Response

from django.conf import settings

from config import celery_app
from .models import Client, Message, MailingList
from .serializers import (
    ClientCreateUpdateSerializer,
    MailingCreateUpdateSerializer, ClientSerializer,
)
from .service.send_mail import send_message
from .tasks import send_message_task


# TODO: Сделать через ViewSet


local_tz = pytz.timezone('Europe/Moscow')


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


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

        date_now = datetime.datetime.now(local_tz)
        date_start = utc_to_local(ml.date_start)
        date_stop = utc_to_local(ml.date_stop)

        print(date_now)
        print(date_start)
        print(date_stop)

        # if date_start < date_now < date_stop:
        clients = Client.objects.filter(
            Q(tag=ml.tag) | Q(operator_code=ml.operator_code)
        )
        print(clients)
        new_message = Message.objects.create(
            external_id=uuid.uuid4(),
            create_at=datetime.datetime.now(),
            status=True,
            mailing_list=ml,
        )

        new_message.clients.add(*clients)

        for client in clients:
            send_message_task.apply_async(
                (
                    new_message.pk,
                    ml.text,
                    int(client.phone),
                ),
                {},
                start_time=date_start,
                expires=date_stop
            )
        # else:

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
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
    """ Просмотра списка рассылок
    """
    serializer_class = MailingCreateUpdateSerializer

    def get_queryset(self):
        queryset = MailingList.objects.prefetch_related("messages")
        return queryset

