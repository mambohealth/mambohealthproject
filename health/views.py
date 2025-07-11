from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import HealthRecord, HealthCategory, DiseaseCategory, SymptomLog, Medication, HealthRecordComment
from django.db.models import Q, F, Count
from django.db.models.functions import Cast
from django.db.models.fields import FloatField
from django.shortcuts import render, redirect, get_object_or_404
from collections import defaultdict
from django.views.decorators.http import require_POST
from .forms import HealthRecordForm, HealthRecordCommentForm, SymptomLogForm, MedicationForm
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

# --- Chart Data AJAX Endpoint ---
@login_required
def healthrecord_chart_data(request):
    user = request.user
    category_id = request.GET.get('category', '')
    disease_id = request.GET.get('disease', '')
    search_query = request.GET.get('search', '')
    out_of_range_filter = request.GET.get('out_of_range', 'false') == 'true'

    records = HealthRecord.objects.filter(user=user)

    if category_id:
        records = records.filter(category_id=category_id)
    if disease_id:
        records = records.filter(disease_category_id=disease_id)
    if search_query:
        records = records.filter(
            Q(title__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(disease_category__name__icontains=search_query) |
            Q(data__icontains=search_query)
        )

    # Exclude records with non-numeric data before attempting to filter by value
    records = records.exclude(data__isnull=True).exclude(data__exact='')

    if out_of_range_filter:
        # This corrected query explicitly checks that a boundary exists before comparing against it.
        records = records.annotate(
            data_float=Cast('data', FloatField()),
            normal_min_float=Cast('normal_min', FloatField()),
            normal_max_float=Cast('normal_max', FloatField())
        ).filter(
            Q(normal_min__isnull=False, normal_min__gt='', data_float__lt=F('normal_min_float')) |
            Q(normal_max__isnull=False, normal_max__gt='', data_float__gt=F('normal_max_float'))
        )

    records = records.order_by('date')
    
    datasets = defaultdict(lambda: {'label': '', 'data': [], 'normal_min': None, 'normal_max': None, 'unit': None})

    for r in records:
        title = r.title
        if not datasets[title]['label']:
            datasets[title]['label'] = title
            datasets[title]['normal_min'] = r.normal_min
            datasets[title]['normal_max'] = r.normal_max
            datasets[title]['unit'] = r.unit

        try:
            value = float(r.data)
            min_val = float(r.normal_min) if r.normal_min is not None and r.normal_min != '' else None
            max_val = float(r.normal_max) if r.normal_max is not None and r.normal_max != '' else None
            out_of_range = False
            if min_val is not None and value < min_val:
                out_of_range = True
            if max_val is not None and value > max_val:
                out_of_range = True
            # Only include out-of-range values if filter is active
            if out_of_range_filter:
                if out_of_range:
                    datasets[title]['data'].append({
                        'x': r.date.strftime('%Y-%m-%d'),
                        'y': value,
                        'out_of_range': out_of_range,
                        'comments': '\n'.join([c.comment for c in r.comments.all()])
                    })
            else:
                datasets[title]['data'].append({
                    'x': r.date.strftime('%Y-%m-%d'),
                    'y': value,
                    'out_of_range': out_of_range,
                    'comments': '\n'.join([c.comment for c in r.comments.all()])
                })
        except (TypeError, ValueError):
            continue

    return JsonResponse({'datasets': list(datasets.values())})


# Inline AJAX update for HealthRecord
@login_required
@require_POST
def healthrecord_inline_update(request, pk):
    record = get_object_or_404(HealthRecord, pk=pk, user=request.user)
    field = request.POST.get('field')
    value = request.POST.get('value')
    if field in ['data', 'unit', 'notes']:
        setattr(record, field, value)
        record.save(update_fields=[field, 'updated_at'])
        return JsonResponse({'success': True, 'value': value})
    return JsonResponse({'success': False, 'error': 'Invalid field'})

# AJAX: List comments for a record
@login_required
def healthrecord_comments(request, pk):
    record = get_object_or_404(HealthRecord, pk=pk, user=request.user)
    comments = record.comments.select_related('user').order_by('-created_at')
    data = [
        {
            'user': c.user.username,
            'comment': c.comment,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M'),
        }
        for c in comments
    ]
    return JsonResponse({'comments': data})

# AJAX: Add comment to a record
@login_required
@require_POST
def healthrecord_comment_add(request, pk):
    record = get_object_or_404(HealthRecord, pk=pk, user=request.user)
    comment = request.POST.get('comment', '').strip()
    if comment:
        HealthRecordComment.objects.create(record=record, user=request.user, comment=comment)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Empty comment'})

# Symptom Log Delete
@login_required
def symptomlog_delete(request, pk):
    log = get_object_or_404(SymptomLog, pk=pk, user=request.user)
    if request.method == 'POST':
        log.delete()
        return redirect('health:symptomlog_list')
    return render(request, 'health/confirm_delete.html', {'object': log, 'type': 'Symptom Log'})

# Medication Delete
@login_required
def medication_delete(request, pk):
    med = get_object_or_404(Medication, pk=pk, user=request.user)
    if request.method == 'POST':
        med.delete()
        return redirect('health:medication_list')
    return render(request, 'health/confirm_delete.html', {'object': med, 'type': 'Medication'})

# Symptom Log Views
@login_required
def symptomlog_list(request):
    logs = SymptomLog.objects.filter(user=request.user).order_by('-date')
    return render(request, 'health/symptomlog_list.html', {'logs': logs})

@login_required
def symptomlog_create(request):
    if request.method == 'POST':
        form = SymptomLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect('health:symptomlog_list')
    else:
        form = SymptomLogForm()
    return render(request, 'health/symptomlog_form.html', {'form': form})

# Medication Views
@login_required
def medication_list(request):
    meds = Medication.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'health/medication_list.html', {'meds': meds})

@login_required
def medication_create(request):
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            med = form.save(commit=False)
            med.user = request.user
            med.save()
            return redirect('health:medication_list')
    else:
        form = MedicationForm()
    return render(request, 'health/medication_form.html', {'form': form})

@login_required
def bulk_rename_title(request):
    if request.method == 'POST':
        old_title = request.POST.get('old_title', '').strip()
        new_title = request.POST.get('new_title', '').strip()
        if old_title and new_title:
            count = HealthRecord.objects.filter(user=request.user, title=old_title).update(title=new_title)
            messages.success(request, f'Renamed {count} records from "{old_title}" to "{new_title}".')
        else:
            messages.error(request, 'Both old and new title are required.')
        return HttpResponseRedirect(reverse('health:healthrecord_list'))
    return HttpResponseRedirect(reverse('health:healthrecord_list'))

@login_required
def bulk_edit_by_title(request):
    if request.method == 'POST':
        title = request.POST.get('edit_title', '').strip()
        category_id = request.POST.get('edit_category', '')
        disease_category_id = request.POST.get('edit_disease_category', '')
        unit = request.POST.get('edit_unit', '').strip()
        normal_min = request.POST.get('edit_normal_min', '').strip()
        normal_max = request.POST.get('edit_normal_max', '').strip()
        update_fields = {}
        if category_id:
            update_fields['category_id'] = category_id
        if disease_category_id:
            update_fields['disease_category_id'] = disease_category_id
        if unit:
            update_fields['unit'] = unit
        if normal_min:
            update_fields['normal_min'] = normal_min
        if normal_max:
            update_fields['normal_max'] = normal_max
        if title and update_fields:
            count = HealthRecord.objects.filter(user=request.user, title=title).update(**update_fields)
            messages.success(request, f'Updated {count} records with title "{title}".')
        else:
            messages.error(request, 'Title and at least one field to update are required.')
        return HttpResponseRedirect(reverse('health:healthrecord_list'))
    return HttpResponseRedirect(reverse('health:healthrecord_list'))


@login_required
def healthrecord_list(request):
    records = HealthRecord.objects.filter(user=request.user).annotate(comment_count=Count('comments'))

    # Filtering
    search = request.GET.get('search', '').strip()
    sort = request.GET.get('sort', '-date')
    category_id = request.GET.get('category', '')
    disease_category_id = request.GET.get('disease_category', '')
    out_of_range = request.GET.get('out_of_range', 'off') == 'on'

    if search:
        records = records.filter(
            Q(title__icontains=search) |
            Q(category__name__icontains=search) |
            Q(disease_category__name__icontains=search) |
            Q(data__icontains=search)
        )
    if category_id:
        records = records.filter(category_id=category_id)
    if disease_category_id:
        records = records.filter(disease_category_id=disease_category_id)
    
    if out_of_range:
        records = records.exclude(data__isnull=True).exclude(data__exact='').exclude(data='None').annotate(
            data_float=Cast('data', FloatField()),
            normal_min_float=Cast('normal_min', FloatField()),
            normal_max_float=Cast('normal_max', FloatField())
        ).filter(
            Q(normal_min__isnull=False, normal_min__gt='', data_float__lt=F('normal_min_float')) |
            Q(normal_max__isnull=False, normal_max__gt='', data_float__gt=F('normal_max_float'))
        )

    # Sorting
    allowed_sorts = ['date', '-date', 'title', '-title', 'data', '-data']
    if sort in allowed_sorts:
        records = records.order_by(sort)
    else:
        records = records.order_by('-date')

    # Bulk delete
    if request.method == 'POST' and 'delete_date' in request.POST:
        del_date = request.POST.get('delete_date')
        if del_date:
            HealthRecord.objects.filter(user=request.user, date=del_date).delete()
            records = records.filter(~Q(date=del_date))

    # Pagination
    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = HealthCategory.objects.all()
    disease_categories = DiseaseCategory.objects.all()
    return render(request, 'health/healthrecord_list.html', {
        'records': page_obj.object_list,
        'page_obj': page_obj,
        'search': search,
        'sort': sort,
        'categories': categories,
        'disease_categories': disease_categories,
        'selected_category': category_id,
        'selected_disease_category': disease_category_id,
        'out_of_range': out_of_range,
    })

@login_required
def healthrecord_create(request):
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return redirect('health:healthrecord_list')
    else:
        form = HealthRecordForm()
    return render(request, 'health/healthrecord_form.html', {'form': form})

@login_required
def healthrecord_edit(request, pk):
    record = get_object_or_404(HealthRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HealthRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('health:healthrecord_list')
    else:
        form = HealthRecordForm(instance=record)
    return render(request, 'health/healthrecord_form.html', {'form': form, 'record': record})

@login_required
def healthrecord_delete(request, pk):
    record = get_object_or_404(HealthRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        record.delete()
        return redirect('health:healthrecord_list')
    return render(request, 'health/confirm_delete.html', {'record': record})