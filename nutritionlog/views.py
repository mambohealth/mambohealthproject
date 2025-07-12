from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import NutritionLog
from .forms import NutritionLogForm
import random

# Placeholder for AI analysis
def analyze_meal(image_data=None, notes=None):
    """
    Dummy function to simulate AI analysis of a meal.
    In a real application, this would call an external AI service.
    """
    if image_data or notes:
        # Simulate AI processing and returning nutritional info
        return {
            'calories': round(random.uniform(200, 800), 2),
            'protein': round(random.uniform(10, 50), 2),
            'carbohydrates': round(random.uniform(20, 100), 2),
            'fat': round(random.uniform(5, 40), 2),
        }
    return {}

@login_required
def nutritionlog_list(request):
    if request.method == 'POST':
        form = NutritionLogForm(request.POST, request.FILES)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user

            meal_photo = request.FILES.get('meal_photo')
            notes = form.cleaned_data.get('notes')
            
            # If any of the nutrition fields are empty, try to fill with AI
            if meal_photo or notes:
                # Check if any nutrition field is not filled by the user
                if not all([
                    form.cleaned_data.get('calories'), 
                    form.cleaned_data.get('protein'), 
                    form.cleaned_data.get('carbohydrates'), 
                    form.cleaned_data.get('fat')
                ]):
                    ai_data = analyze_meal(image_data=meal_photo, notes=notes)
                    log.calories = form.cleaned_data.get('calories') or ai_data.get('calories')
                    log.protein = form.cleaned_data.get('protein') or ai_data.get('protein')
                    log.carbohydrates = form.cleaned_data.get('carbohydrates') or ai_data.get('carbohydrates')
                    log.fat = form.cleaned_data.get('fat') or ai_data.get('fat')

            log.save()
            return redirect('nutritionlog_list')
    else:
        form = NutritionLogForm()
    
    log_list = NutritionLog.objects.filter(user=request.user)
    paginator = Paginator(log_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, 'nutritionlog/nutritionlog_list.html', context)