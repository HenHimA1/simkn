from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    search_fields = ["number", "name"]
    ordering = ["id"]
    list_display = ('number', 'name', 'gender', 'age', 'weight', 'height', 'input_date')
