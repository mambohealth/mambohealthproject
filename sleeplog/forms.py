from django import forms
from .models import SleepLog

class SleepLogForm(forms.ModelForm):
    class Meta:
        model = SleepLog
        fields = ['date', 'duration', 'quality', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if not 0 <= duration <= 24:
            raise forms.ValidationError("Duration must be between 0 and 24 hours.")
        return duration

    def clean_quality(self):
        quality = self.cleaned_data.get('quality')
        if not 1 <= quality <= 10:
            raise forms.ValidationError("Quality must be an integer between 1 and 10.")
        return quality
