from django.db import models
from django.contrib.auth import get_user_model
from wagtail.snippets.models import register_snippet

@register_snippet
class HealthCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

@register_snippet
class DiseaseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class HealthRecord(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateField()
    category = models.ForeignKey(HealthCategory, on_delete=models.SET_NULL, null=True, blank=True)
    disease_category = models.ForeignKey(DiseaseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    data = models.CharField(max_length=100, blank=True)  # value field
    unit = models.CharField(max_length=50, blank=True)
    normal_min = models.CharField(max_length=50, blank=True)
    normal_max = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.date})"
