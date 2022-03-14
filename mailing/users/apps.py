from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "mailing.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import mailing.users.signals  # noqa F401
        except ImportError:
            pass
