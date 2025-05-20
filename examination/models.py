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
    
class Diagnosis(models.Model):
    name = models.CharField(max_length=100)
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class SequenceCT(models.Model):
    name = models.CharField(max_length=100)
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

# Create your models here.
class SPECT(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.PROTECT, verbose_name="Patient")
    exam_date = models.DateTimeField()
    inject_date = models.DateTimeField(null=True, blank=True)
    diagnosis_id = models.ForeignKey(Diagnosis, on_delete=models.PROTECT, verbose_name="Diagnosis", null=True, blank=True)
    procedure_id = models.ForeignKey(Procedure, on_delete=models.PROTECT, verbose_name="Procedure", null=True)
    radionuclide_id = models.ForeignKey(Radionuclide, on_delete=models.PROTECT, verbose_name="Radionuclide", null=True)
    pharmaceutical_id = models.ForeignKey(Pharmaceutical, on_delete=models.PROTECT, verbose_name="pharmaceutical", null=True)
    activity_post_injection = models.FloatField(null=True, help_text="mCi", verbose_name="Post injection")
    activity_pre_injection = models.FloatField(null=True, help_text="mCi", verbose_name="Pre injection")
    sequence_ct = models.ManyToManyField(SequenceCT, blank=True, verbose_name="Sequence CT")
    input_date = models.DateTimeField(auto_now_add=True, null=True)
    ctdi = models.FloatField(default=0, help_text="mGy", verbose_name="CTDI")
    dlp = models.FloatField(default=0, help_text="mGy.cm", verbose_name="DLP")
    location_id = models.ForeignKey(Location, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Location")

    def __str__(self):
        return f"{self.patient_id.name}"
    
    class Meta:
        verbose_name_plural = "SPECT"