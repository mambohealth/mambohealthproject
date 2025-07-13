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
            'meal_type': forms.Select(attrs={
                'class': 'block appearance-none w-full bg-white border border-gray-300 text-gray-700 py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
            }),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'meal_photo': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'calories': forms.NumberInput(attrs={'class': 'form-input'}),
            'protein': forms.NumberInput(attrs={'class': 'form-input'}),
            'carbohydrates': forms.NumberInput(attrs={'class': 'form-input'}),
            'fat': forms.NumberInput(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(NutritionLogForm, self).__init__(*args, **kwargs)
        self.fields['meal_type'].empty_label = "Select a meal type"

    def clean_meal_type(self):
        meal_type = self.cleaned_data.get('meal_type')
        if not meal_type:
            raise forms.ValidationError("This field is required.")
        return meal_type
