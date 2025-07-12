from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import SleepLog
from .forms import SleepLogForm

@login_required
def sleeplog_list(request):
    if request.method == 'POST':
        form = SleepLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect('sleeplog_list')
    else:
        form = SleepLogForm()
    
    log_list = SleepLog.objects.filter(user=request.user)
    paginator = Paginator(log_list, 10)  # Show 10 logs per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, 'sleeplog/sleeplog_list.html', context)


