import csv

from datetime import date
from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    actions = ['export_as_csv']
    search_fields = ["number", "name"]
    ordering = ["id"]
    list_display = ('number', 'name', 'gender', 'age', 'weight', 'height', 'input_date')

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