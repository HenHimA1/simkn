from django.contrib import admin
from .models import Patient, Insurance

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    autocomplete_fields = ["insurance_id"]
    search_fields = ["number", "name"]
    list_display = ('number', 'name', 'sex', 'age', 'weight', 'height', 'input_date')

@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    search_fields = ['name']