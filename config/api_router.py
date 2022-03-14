from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from mailing.users.api.views import UserViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)

urlpatterns = [
    path("mailing/", include("mailing.mail.urls"))
]


app_name = "api"
urlpatterns += router.urls
