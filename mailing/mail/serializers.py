import uuid

from rest_framework import serializers

from .models import Client, MailingList, Message


class ClientCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        exclude = ["id"]


class MailingSerializer(serializers.ModelSerializer):

    class Meta:
        model = MailingList
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    # clients = ClientSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = "__all__"


class MailingCreateUpdateSerializer(serializers.ModelSerializer):
    # external_id = serializers.UUIDField(default=uuid.uuid4())
    # date_start = serializers.DateTimeField(required=True)
    # text = serializers.CharField(max_length=500, required=True)
    # date_stop = serializers.DateTimeField()

    class Meta:
        model = MailingList
        fields = [
            "external_id",
            "date_start",
            "text",
            "date_stop",
            "operator_code",
            "tag"
        ]


