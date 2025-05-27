import csv
import logging

from datetime import date
from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
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
    actions = ['export_as_csv']
    search_fields = ["patient__name", "procedure__name"]
    ordering = ["id"]
    autocomplete_fields = ["patient", "radionuclide", "pharmaceutical", "procedure", "diagnosis", "location", "sequence_ct"]
    list_display = ["procedure", "radionuclide", "patient", "exam_date", "input_date"]
    list_filter = ["procedure", "radionuclide", "exam_date"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta.verbose_name}-{date.today()}.csv'
        writer = csv.writer(response)

        # Header
        writer.writerow(field_names)

        # Rows
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = _("Export selected to CSV")

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
    actions = ['export_as_csv']
    search_fields = ["patient__name", "procedure__name"]
    ordering = ["id"]
    autocomplete_fields = ["patient", "radionuclide", "pharmaceutical", "procedure", "diagnosis", "location", "sequence_ct"]
    list_display = ["procedure", "radionuclide", "patient", "exam_date", "input_date"]
    list_filter = ["procedure", "radionuclide", "exam_date"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta.verbose_name}-{date.today()}.csv'
        writer = csv.writer(response)

        # Header
        writer.writerow(field_names)

        # Rows
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = _("Export selected to CSV")