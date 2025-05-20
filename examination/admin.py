import logging
from django.contrib import admin
from .models import SPECT, PET, PETRadionuclide, PETPharmaceutical, PETProcedure, PETDiagnosis, SPECTDiagnosis, SPECTPharmaceutical, SPECTProcedure, SPECTRadionuclide, SequenceCT, Location
# Register your models here.

_logger = logging.getLogger(__name__)

@admin.register(SPECTRadionuclide)
class SPECTRadionuclideAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["id"]

@admin.register(SPECTPharmaceutical)
class SPECTPharmaceuticalAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["id"]

@admin.register(SPECTDiagnosis)
class SPECTDiagnosisAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["id"]

@admin.register(SPECTProcedure)
class SPECTProcedureAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["id"]

@admin.register(SPECT)
class SPECTAdmin(admin.ModelAdmin):
    search_fields = ["patient__name", "procedure__name"]
    ordering = ["id"]
    autocomplete_fields = ["patient", "radionuclide", "pharmaceutical", "procedure", "diagnosis", "location", "sequence_ct"]
    list_display = ["procedure", "radionuclide", "patient", "exam_date", "input_date"]
    list_filter = ["procedure", "radionuclide"]


@admin.register(PETRadionuclide)
class PETRadionuclideAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["id"]
    
@admin.register(PETPharmaceutical)
class PETPharmaceuticalAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["id"]
    
@admin.register(PETDiagnosis)
class PETDiagnosisAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["id"]

@admin.register(PETProcedure)
class PETProcedureAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["id"]

@admin.register(SequenceCT)
class SequenceCTAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["id"]

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["id"]

@admin.register(PET)
class PETAdmin(admin.ModelAdmin):
    search_fields = ["patient__name", "procedure__name"]
    ordering = ["id"]
    autocomplete_fields = ["patient", "radionuclide", "pharmaceutical", "procedure", "diagnosis", "location", "sequence_ct"]
    list_display = ["procedure", "radionuclide", "patient", "exam_date", "input_date"]
    list_filter = ["procedure", "radionuclide"]
