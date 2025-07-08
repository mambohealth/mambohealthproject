from django.contrib import admin
from .models import HealthCategory, DiseaseCategory, HealthRecord, HealthRecordComment, SymptomLog, Medication

@admin.register(HealthRecordComment)
class HealthRecordCommentAdmin(admin.ModelAdmin):
    list_display = ('record', 'user', 'created_at')
    search_fields = ('comment',)
    autocomplete_fields = ['record', 'user']
    readonly_fields = ('created_at', 'updated_at')

@admin.register(SymptomLog)
class SymptomLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'symptom', 'severity', 'created_at')
    search_fields = ('symptom', 'notes')
    autocomplete_fields = ['user']
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'dosage', 'frequency', 'start_date', 'end_date', 'created_at')
    search_fields = ('name', 'notes')
    autocomplete_fields = ['user']
    readonly_fields = ('created_at', 'updated_at')

@admin.register(HealthCategory)
class HealthCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(DiseaseCategory)
class DiseaseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date', 'category', 'disease_category', 'created_at')
    list_filter = ('category', 'disease_category', 'date')
    search_fields = ('title', 'notes', 'tags')
    autocomplete_fields = ['user', 'category', 'disease_category']
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')
