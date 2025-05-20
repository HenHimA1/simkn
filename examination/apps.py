from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class ExaminationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'examination'

    def ready(self):
        self.verbose_name = _('examination')
        return super().ready()