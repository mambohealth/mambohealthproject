from django.db import models
from django.conf import settings

class Food(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="e.g., 'Chicken Salad', 'Apple'")
    calories = models.FloatField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True, help_text="in grams")
    carbohydrates = models.FloatField(blank=True, null=True, help_text="in grams")
    fat = models.FloatField(blank=True, null=True, help_text="in grams")
    saturated_fat = models.FloatField(blank=True, null=True, help_text="in grams")
    cholesterol = models.FloatField(blank=True, null=True, help_text="in milligrams")
    sodium = models.FloatField(blank=True, null=True, help_text="in milligrams")
    potassium = models.FloatField(blank=True, null=True, help_text="in milligrams")
    fiber = models.FloatField(blank=True, null=True, help_text="in grams")
    sugars = models.FloatField(blank=True, null=True, help_text="in grams")
    vitamin_c = models.FloatField(blank=True, null=True, help_text="in milligrams")
    omega3_epa_dha = models.FloatField(blank=True, null=True, help_text="in milligrams", verbose_name="Omega-3 (EPA/DHA)")

    def __str__(self):
        return self.name

class NutritionLog(models.Model):
    MEAL_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
        ('Drink', 'Drink'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=10, choices=MEAL_CHOICES)
    name = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 'Chicken Salad', 'Apple'")
    ingredients = models.TextField(blank=True, null=True, help_text="Describe the ingredients for a more accurate nutrition analysis.")
    notes = models.TextField(blank=True, null=True)
    meal_photo = models.ImageField(upload_to='meal_photos/', blank=True, null=True)
    calories = models.FloatField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True, help_text="in grams")
    carbohydrates = models.FloatField(blank=True, null=True, help_text="in grams")
    fat = models.FloatField(blank=True, null=True, help_text="in grams")
    saturated_fat = models.FloatField(blank=True, null=True, help_text="in grams")
    cholesterol = models.FloatField(blank=True, null=True, help_text="in milligrams")
    sodium = models.FloatField(blank=True, null=True, help_text="in milligrams")
    potassium = models.FloatField(blank=True, null=True, help_text="in milligrams")
    fiber = models.FloatField(blank=True, null=True, help_text="in grams")
    sugars = models.FloatField(blank=True, null=True, help_text="in grams")
    vitamin_c = models.FloatField(blank=True, null=True, help_text="in milligrams")
    omega3_epa_dha = models.FloatField(blank=True, null=True, help_text="in milligrams", verbose_name="Omega-3 (EPA/DHA)")

    DATA_SOURCE_CHOICES = [
        ('USER_INPUT', 'User Input'),
        ('PHOTO_ANALYSIS', 'Photo Analysis'),
        ('TYPICAL_DATA', 'Typical Data'),
        ('NOTES_ANALYSIS', 'Notes Analysis'),
        ('INGREDIENTS_ANALYSIS', 'Ingredients Analysis'),
    ]
    data_source = models.CharField(max_length=20, choices=DATA_SOURCE_CHOICES, default='USER_INPUT')

    def __str__(self):
        return f"{self.get_meal_type_display()} for {self.user.username} on {self.date}"

    class Meta:
        ordering = ['-date']