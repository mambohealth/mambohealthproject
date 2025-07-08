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
            'date', 'category', 'disease_category', 'title', 'notes', 'data', 'tags'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.TextInput(attrs={'placeholder': 'e.g. blood, cholesterol'}),
        }
