# Generated by Django 5.2.4 on 2025-07-13 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutritionlog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nutritionlog',
            name='cholesterol',
            field=models.FloatField(blank=True, help_text='in milligrams', null=True),
        ),
        migrations.AddField(
            model_name='nutritionlog',
            name='fiber',
            field=models.FloatField(blank=True, help_text='in grams', null=True),
        ),
        migrations.AddField(
            model_name='nutritionlog',
            name='potassium',
            field=models.FloatField(blank=True, help_text='in milligrams', null=True),
        ),
        migrations.AddField(
            model_name='nutritionlog',
            name='saturated_fat',
            field=models.FloatField(blank=True, help_text='in grams', null=True),
        ),
        migrations.AddField(
            model_name='nutritionlog',
            name='sodium',
            field=models.FloatField(blank=True, help_text='in milligrams', null=True),
        ),
        migrations.AddField(
            model_name='nutritionlog',
            name='sugars',
            field=models.FloatField(blank=True, help_text='in grams', null=True),
        ),
    ]
