from django.urls import path

from .views import (
    CreateClientView,
    UpdateClientView,
    DestroyClientView,
    MailingCreateView,
    MailingUpdateView,
    MailingDestroyView,

    MailingListView,
    MailingListClientsListView
)


urlpatterns = [
    path("create-client/", CreateClientView.as_view(), name="create-client"),
    path("update-client/<int:id>/", UpdateClientView.as_view(), name="update-client"),
    path("destroy-client/<int:id>/", DestroyClientView.as_view(), name="destroy-client"),

    path("create-mailing/", MailingCreateView.as_view(), name="create-mailing"),
    path("update-mailing/<int:id>/", MailingUpdateView.as_view(), name="update-mailing"),
    path("destroy-mailing/<int:id>/", MailingDestroyView.as_view(), name="destroy-mailing"),
    path("list-mailing/", MailingListView.as_view(), name="list-mailing"),
    path("list-clients-mailing/<int:id>/", MailingListClientsListView.as_view(), name="list-clients-mailing"),
]

