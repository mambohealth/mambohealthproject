from django import forms
from .models import HealthRecord, HealthRecordComment, SymptomLog, Medication

class HealthRecordCommentForm(forms.ModelForm):
    class Meta:
        model = HealthRecordComment
        fields = ['comment']

class SymptomLogForm(forms.ModelForm):
    class Meta:
        model = SymptomLog
        fields = ['date', 'symptom', 'severity', 'notes']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'dosage', 'frequency', 'start_date', 'end_date', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = [
            'date', 'category', 'disease_category', 'title', 'data', 'unit', 'normal_min', 'normal_max', 'tags', 'notes'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-textarea'}),
            'tags': forms.TextInput(attrs={'placeholder': 'e.g. blood, cholesterol', 'class': 'form-input'}),
            'data': forms.TextInput(attrs={'class': 'form-input'}),
            'unit': forms.TextInput(attrs={'class': 'form-input'}),
            'normal_min': forms.TextInput(attrs={'class': 'form-input'}),
            'normal_max': forms.TextInput(attrs={'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input'}),
        }
