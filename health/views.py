from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import HealthRecord, HealthCategory, DiseaseCategory
from .forms import HealthRecordForm
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def healthrecord_list(request):
    records = HealthRecord.objects.filter(user=request.user)


    # Filtering
    search = request.GET.get('search', '').strip()
    sort = request.GET.get('sort', '-date')
    category_id = request.GET.get('category', '')
    disease_category_id = request.GET.get('disease_category', '')

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
    return render(request, 'health/healthrecord_confirm_delete.html', {'record': record})
