from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class RegistrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'registration'

    def ready(self):
        self.verbose_name = _("registration")
        return super().ready()