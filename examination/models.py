from django.utils.translation import gettext_lazy as _
from django.db import models
from registration.models import Patient

class Radionuclide(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Pharmaceutical(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class Procedure(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class Diagnosis(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class SequenceCT(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

# Create your models here.
class SPECT(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.PROTECT, verbose_name=_("Patient"))
    exam_date = models.DateTimeField(verbose_name=_("Exam date"))
    inject_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Inject date"))
    diagnosis_id = models.ForeignKey(Diagnosis, on_delete=models.PROTECT, verbose_name=_("Diagnosis"), null=True, blank=True)
    procedure_id = models.ForeignKey(Procedure, on_delete=models.PROTECT, verbose_name=_("Procedure"), null=True)
    radionuclide_id = models.ForeignKey(Radionuclide, on_delete=models.PROTECT, verbose_name=_("Radionuclide"), null=True)
    pharmaceutical_id = models.ForeignKey(Pharmaceutical, on_delete=models.PROTECT, verbose_name=_("pharmaceutical"), null=True)
    activity_post_injection = models.FloatField(null=True, help_text="mCi", verbose_name=_("Post injection"))
    activity_pre_injection = models.FloatField(null=True, help_text="mCi", verbose_name=_("Pre injection"))
    sequence_ct = models.ManyToManyField(SequenceCT, blank=True, verbose_name=_("Sequence CT"))
    input_date = models.DateTimeField(auto_now_add=True, null=True)
    ctdi = models.FloatField(default=0, help_text="mGy", verbose_name=_("CTDI"))
    dlp = models.FloatField(default=0, help_text="mGy.cm", verbose_name=_("DLP"))
    location_id = models.ForeignKey(Location, on_delete=models.PROTECT, null=True, blank=True, verbose_name=_("Location"))

    def __str__(self):
        return f"{self.patient_id.name}"
    
    class Meta:
        verbose_name_plural = "SPECT"