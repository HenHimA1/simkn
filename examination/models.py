from django.utils.translation import gettext_lazy as _
from django.db import models
from registration.models import Patient

class SPECTRadionuclide(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

class SPECTPharmaceutical(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class SPECTProcedure(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class SPECTDiagnosis(models.Model):
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
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, verbose_name=_("Patient"))
    exam_date = models.DateTimeField(verbose_name=_("Exam date"))
    inject_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Inject date"))
    diagnosis = models.ForeignKey(SPECTDiagnosis, on_delete=models.PROTECT, verbose_name=_("Diagnosis"), null=True, blank=True)
    procedure = models.ForeignKey(SPECTProcedure, on_delete=models.PROTECT, verbose_name=_("Procedure"), null=True)
    radionuclide = models.ForeignKey(SPECTRadionuclide, on_delete=models.PROTECT, verbose_name=_("Radionuclide"), null=True)
    pharmaceutical = models.ForeignKey(SPECTPharmaceutical, on_delete=models.PROTECT, verbose_name=_("Pharmaceutical"), null=True)
    activity_post_injection = models.FloatField(default=0, null=True, help_text="mCi", verbose_name=_("Post injection"))
    activity_pre_injection = models.FloatField(default=0, null=True, help_text="mCi", verbose_name=_("Pre injection"))
    sequence_ct = models.ManyToManyField(SequenceCT, blank=True, verbose_name=_("Sequence CT"))
    input_date = models.DateTimeField(auto_now_add=True, null=True)
    ctdi = models.FloatField(default=0, help_text="mGy", verbose_name=_("CTDI"))
    dlp = models.FloatField(default=0, help_text="mGy.cm", verbose_name=_("DLP"))
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True, blank=True, verbose_name=_("Location"))

    def __str__(self):
        return f"{self.patient.name}"
    
    class Meta:
        verbose_name = _("SPECT")
        verbose_name_plural = _("SPECTs")

class PETRadionuclide(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

class PETPharmaceutical(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class PETProcedure(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class PETDiagnosis(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    input_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

class PET(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, verbose_name=_("Patient"))
    exam_date = models.DateTimeField(verbose_name=_("Exam date"))
    inject_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Inject date"))
    diagnosis = models.ForeignKey(PETDiagnosis, on_delete=models.PROTECT, verbose_name=_("Diagnosis"), null=True, blank=True)
    procedure = models.ForeignKey(PETProcedure, on_delete=models.PROTECT, verbose_name=_("Procedure"), null=True)
    radionuclide = models.ForeignKey(PETRadionuclide, on_delete=models.PROTECT, verbose_name=_("Radionuclide"), null=True)
    pharmaceutical = models.ForeignKey(PETPharmaceutical, on_delete=models.PROTECT, verbose_name=_("Pharmaceutical"), null=True)
    activity_post_injection = models.FloatField(default=0, null=True, help_text="mCi", verbose_name=_("Post injection"))
    activity_pre_injection = models.FloatField(default=0, null=True, help_text="mCi", verbose_name=_("Pre injection"))
    sequence_ct = models.ManyToManyField(SequenceCT, blank=True, verbose_name=_("Sequence CT"))
    input_date = models.DateTimeField(auto_now_add=True, null=True)
    ctdi = models.FloatField(default=0, help_text="mGy", verbose_name=_("CTDI"))
    dlp = models.FloatField(default=0, help_text="mGy.cm", verbose_name=_("DLP"))
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True, blank=True, verbose_name=_("Location"))
    exposure_rate = models.FloatField(default=0, verbose_name=_("Exposure rate"), help_text="mR/h")

    def __str__(self):
        return f"{self.patient.name}"
    
    class Meta:
        verbose_name = _("PET")
        verbose_name_plural = _("PETs")