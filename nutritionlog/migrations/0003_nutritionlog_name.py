# Generated by Django 5.2.4 on 2025-07-13 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutritionlog', '0002_nutritionlog_cholesterol_nutritionlog_fiber_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='nutritionlog',
            name='name',
            field=models.CharField(blank=True, help_text="e.g., 'Chicken Salad', 'Apple'", max_length=100, null=True),
        ),
    ]
