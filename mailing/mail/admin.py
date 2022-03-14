from django.contrib import admin

from .models import MailingList, Message, Client


admin.site.register(MailingList)
admin.site.register(Message)
admin.site.register(Client)
