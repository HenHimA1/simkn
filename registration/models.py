from django.utils.translation import gettext_lazy as _
from django.db import models
from datetime import date

class Patient(models.Model):
    number = models.CharField(max_length=100, unique=True, verbose_name=_("Number"), null=True)
    name = models.CharField(max_length=100, verbose_name=_("Name"), null=True)
    birth_date = models.DateField(verbose_name=_("Birth date"))
    gender = models.CharField(max_length=1, choices=[("M", _("Male")), ("F", _("Female"))], null=True, verbose_name=_("Gender"))
    weight = models.FloatField(help_text="kg", verbose_name=_("Weight"))
    height = models.FloatField(help_text="cm", verbose_name=_("Height"))
    input_date = models.DateTimeField(auto_now_add=True)

    @property
    def age(self):
        today = date.today()
        if self.birth_date:
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None

    def __str__(self):
        return f"{self.number}-{self.name}"
    
    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patient")
