import datetime

from rest_framework import generics

from .models import Client, Message, MailingList
from .serializers import (
    ClientCreateUpdateSerializer,
    MailingCreateUpdateSerializer,
)


# TODO: Сделать через ViewSet


# Client
from .service.send_mail import send_message


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

    def get_queryset(self):
        queryset = MailingList.objects.all()


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


class MailingView(generics.ListAPIView):
    serializer_class = MailingCreateUpdateSerializer

    def get_queryset(self):
        response = send_message(1, 123123, "qweqwe")
        print(response.json())
        queryset = MailingList.objects.all()
        return queryset

