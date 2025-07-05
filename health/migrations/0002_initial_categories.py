from django.db import migrations

def create_initial_categories(apps, schema_editor):
    HealthCategory = apps.get_model('health', 'HealthCategory')
    DiseaseCategory = apps.get_model('health', 'DiseaseCategory')

    health_categories = [
        ('Cardiovascular', 'Heart and blood vessel health'),
        ('Metabolic', 'Metabolism and related conditions'),
        ('Renal', 'Kidney health'),
        ('Respiratory', 'Lung and breathing health'),
        ('Neurological', 'Brain and nervous system'),
        ('Musculoskeletal', 'Bones, muscles, joints'),
        ('Digestive', 'Stomach, liver, intestines'),
        ('Endocrine', 'Hormones and glands'),
        ('Immunological', 'Immune system'),
        ('General', 'General health'),
    ]
    for name, desc in health_categories:
        HealthCategory.objects.get_or_create(name=name, defaults={'description': desc})

    disease_categories = [
        ('Diabetes', 'Diabetes and related disorders'),
        ('Hypertension', 'High blood pressure'),
        ('Coronary Artery Disease', 'Heart disease'),
        ('Chronic Kidney Disease', 'Kidney disease'),
        ('Asthma', 'Asthma and related conditions'),
        ('COPD', 'Chronic Obstructive Pulmonary Disease'),
        ('Osteoporosis', 'Bone health'),
        ('Arthritis', 'Joint health'),
        ('Cancer', 'Oncology'),
        ('Other', 'Other diseases'),
    ]
    for name, desc in disease_categories:
        DiseaseCategory.objects.get_or_create(name=name, defaults={'description': desc})

class Migration(migrations.Migration):
    dependencies = [
        ('health', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_categories),
    ]
