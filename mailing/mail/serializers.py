from rest_framework.serializers import ModelSerializer

from .models import Client, MailingList


class ClientCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Client
        exclude = ["id"]


class MailingCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = MailingList
        exclude = ["id"]

