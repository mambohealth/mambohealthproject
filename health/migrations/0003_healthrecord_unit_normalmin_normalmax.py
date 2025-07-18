# Generated by Django for health app - migration for new HealthRecord fields
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("health", "0002_initial_categories"),
    ]

    operations = [
        migrations.AddField(
            model_name="healthrecord",
            name="unit",
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name="healthrecord",
            name="normal_min",
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name="healthrecord",
            name="normal_max",
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name="healthrecord",
            name="data",
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
