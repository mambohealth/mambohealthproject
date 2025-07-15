from django import forms
from .models import NutritionLog, Food

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = [
            'name', 
            'calories', 
            'protein', 
            'carbohydrates', 
            'fat',
            'saturated_fat',
            'cholesterol',
            'sodium',
            'potassium',
            'fiber',
            'sugars',
            'vitamin_c',
            'omega3_epa_dha',
        ]

class NutritionLogForm(forms.ModelForm):
    saved_food = forms.ModelChoiceField(
        queryset=Food.objects.none(), 
        required=False,
        label="Or select a saved food"
    )

    class Meta:
        model = NutritionLog
        fields = [
            'date', 
            'meal_type', 
            'name',
            'saved_food',
            'ingredients',
            'notes', 
            'meal_photo', 
            'calories', 
            'protein', 
            'carbohydrates', 
            'fat',
            'saturated_fat',
            'cholesterol',
            'sodium',
            'potassium',
            'fiber',
            'sugars',
            'vitamin_c',
            'omega3_epa_dha',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),            
            'meal_type': forms.Select(attrs={
                'class': 'block appearance-none w-full bg-white border border-gray-300 text-gray-700 py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
            }),
            'ingredients': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'meal_photo': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'calories': forms.NumberInput(attrs={'class': 'form-input'}),
            'protein': forms.NumberInput(attrs={'class': 'form-input'}),
            'carbohydrates': forms.NumberInput(attrs={'class': 'form-input'}),
            'fat': forms.NumberInput(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NutritionLogForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['saved_food'].queryset = Food.objects.filter(user=user)
        
        self.fields['meal_type'].empty_label = "Select a meal type"

    def clean_meal_type(self):
        meal_type = self.cleaned_data.get('meal_type')
        if not meal_type:
            raise forms.ValidationError("This field is required.")
        return meal_type