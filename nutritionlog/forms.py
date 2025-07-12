from django import forms
from .models import NutritionLog

class NutritionLogForm(forms.ModelForm):
    class Meta:
        model = NutritionLog
        fields = [
            'date', 
            'meal_type', 
            'notes', 
            'meal_photo', 
            'calories', 
            'protein', 
            'carbohydrates', 
            'fat'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(NutritionLogForm, self).__init__(*args, **kwargs)
        self.fields['meal_type'].empty_label = "Select a meal type"

    def clean_meal_type(self):
        meal_type = self.cleaned_data.get('meal_type')
        if not meal_type:
            raise forms.ValidationError("This field is required.")
        return meal_type
