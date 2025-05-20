from django.db import models
from datetime import date

class Insurance(models.Model):
    name = models.CharField(max_length=100)
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Patient(models.Model):
    number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    sex = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")], null=True)
    weight = models.FloatField(help_text="Dalam kg")
    height = models.FloatField(help_text="Dalam cm")
    input_date = models.DateTimeField(auto_now_add=True)
    insurance_id = models.ForeignKey(Insurance, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Insurance")

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
