from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """
    Renders the main dashboard page.
    """
    return render(request, 'home/dashboard.html')
