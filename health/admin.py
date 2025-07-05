from django.contrib import admin
from .models import HealthCategory, DiseaseCategory, HealthRecord

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
