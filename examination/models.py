from django.db import models
from registration.models import Patient

class Radionuclide(models.Model):
    name = models.CharField(max_length=100)
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Pharmaceutical(models.Model):
    name = models.CharField(max_length=100)
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class Procedure(models.Model):
    name = models.CharField(max_length=100)
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

# Create your models here.
class SPECT(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.PROTECT, verbose_name="Patient")
    exam_date = models.DateTimeField()
    procedure_id = models.ForeignKey(Procedure, on_delete=models.PROTECT, verbose_name="Procedure", null=True)
    radionuclide_id = models.ForeignKey(Radionuclide, on_delete=models.PROTECT, verbose_name="Radionuclide", null=True)
    pharmaceutical_id = models.ForeignKey(Pharmaceutical, on_delete=models.PROTECT, verbose_name="pharmaceutical", null=True)
    activity_post_injection = models.FloatField(null=True, help_text="mCi", verbose_name="Post injection")
    activity_pre_injection = models.FloatField(null=True, help_text="mCi", verbose_name="Pre injection")
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.patient_id.name}"