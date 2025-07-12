from django.db import models
from django.conf import settings

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
    notes = models.TextField(blank=True, null=True)
    meal_photo = models.ImageField(upload_to='meal_photos/', blank=True, null=True)
    calories = models.FloatField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True, help_text="in grams")
    carbohydrates = models.FloatField(blank=True, null=True, help_text="in grams")
    fat = models.FloatField(blank=True, null=True, help_text="in grams")

    def __str__(self):
        return f"{self.get_meal_type_display()} for {self.user.username} on {self.date}"

    class Meta:
        ordering = ['-date']