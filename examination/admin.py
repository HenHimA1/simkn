from django.contrib import admin
from .models import SPECT, Radionuclide, Pharmaceutical, Procedure
# Register your models here.

@admin.register(SPECT)
class SPECTAdmin(admin.ModelAdmin):
    search_fields = ["patient_id__name", "procedure_id__name"]
    autocomplete_fields = ["patient_id", "radionuclide_id", "pharmaceutical_id", "procedure_id"]
    list_display = ["procedure_id", "patient_id", "exam_date", "input_date"]

@admin.register(Radionuclide)
class RadionuclideAdmin(admin.ModelAdmin):
    search_fields = ["name"]

@admin.register(Pharmaceutical)
class PharmaceuticalAdmin(admin.ModelAdmin):
    search_fields = ["name"]

@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    search_fields = ["name"]