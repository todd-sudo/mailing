import uuid

from rest_framework import serializers

from .models import Client, MailingList, Message


class ClientCreateUpdateSerializer(serializers.ModelSerializer):
    """ Serializer для Создания, Обновление Клиентов
   """
    class Meta:
        model = Client
        exclude = ["id"]


class ClientSerializer(serializers.ModelSerializer):
    """ Serializer для Клиента
    """
    class Meta:
        model = Client
        fields = "__all__"


class MailingCreateUpdateSerializer(serializers.ModelSerializer):
    """ Serializer для Создания, Обновление, показа Списка Рассылок
    """

    class Meta:
        model = MailingList
        fields = "__all__"


class MessageListSerializer(serializers.ModelSerializer):
    clients = ClientSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ["external_id", "create_at", "status", "clients"]


class MailingDetailSerializer(serializers.ModelSerializer):
    """ Serializer
    """
    messages = MessageListSerializer(many=True, read_only=True)
    count_client = serializers.SerializerMethodField()
    count_message = serializers.SerializerMethodField()

    def get_count_message(self, obj):
        return Message.objects.filter(mailing_list=obj).count()

    def get_count_client(self, obj):
        return Client.objects.filter(messages__mailing_list=obj).count()

    class Meta:
        model = MailingList
        fields = "__all__"
