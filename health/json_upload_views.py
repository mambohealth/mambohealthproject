import json
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import HealthRecord
from .forms import HealthRecordForm

class JSONUploadForm(forms.Form):
    json_file = forms.FileField(label="Upload JSON file")

@login_required
def healthrecord_upload_json(request):
    preview_data = None
    mapped_records = None
    if request.method == 'POST':
        form = JSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = form.cleaned_data['json_file']
            try:
                data = json.load(json_file)
                preview_data = data
                # Expecting a list of records in the new JSON format
                if isinstance(data, list):
                    mapped_records = data
                    request.session['json_upload_data'] = mapped_records
                else:
                    messages.error(request, "Uploaded JSON must be a list of records.")
            except Exception as e:
                messages.error(request, f"Invalid JSON: {e}")
    else:
        form = JSONUploadForm()
    return render(request, 'health/healthrecord_upload_json.html', {
        'form': form,
        'preview_data': preview_data,
        'mapped_records': mapped_records,
    })

@login_required
def healthrecord_confirm_json(request):
    mapped_records = request.session.get('json_upload_data')
    if not mapped_records:
        messages.error(request, "No JSON data to confirm.")
        return redirect('health:healthrecord_upload_json')
    if request.method == 'POST':
        # Bulk create HealthRecord objects for each record
        from .models import HealthCategory, DiseaseCategory
        user = request.user
        for rec in mapped_records:
            cat, _ = HealthCategory.objects.get_or_create(name=rec.get('health_catagory', 'Other'))
            dis_cat, _ = DiseaseCategory.objects.get_or_create(name=rec.get('disease_category', 'Other'))
            HealthRecord.objects.create(
                user=user,
                date=rec.get('date'),
                category=cat,
                disease_category=dis_cat,
                title=rec.get('title'),
                data=rec.get('data', ''),
                unit=rec.get('unit', ''),
                normal_min=rec.get('normal_min', ''),
                normal_max=rec.get('normal_max', ''),
                notes='',
                tags='',
            )
        del request.session['json_upload_data']
        messages.success(request, "Health records imported successfully.")
        return redirect('health:healthrecord_list')
    return render(request, 'health/healthrecord_confirm_json.html', {
        'records': mapped_records,
    })
